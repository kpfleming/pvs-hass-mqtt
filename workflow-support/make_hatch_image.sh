#!/usr/bin/env bash

set -ex

projname="pvs-hass-mqtt"

scriptdir=$(realpath "$(dirname "${BASH_SOURCE[0]}")")

py_deps=(build-essential libreadline-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev)
lint_deps=(shellcheck)
proj_deps=(libsystemd0 libsqlite3-0)
proj_build_deps=(pkg-config libsystemd-dev)

pyversions=(3.8.13 3.9.13 3.10.6 3.11.0rc1)

hatchenvs=(lint ci ci-systemd)
cimatrix=(py3.8 py3.9 py3.10 py3.11)

# reviewdog_version="0.14.1"

c=$(buildah from debian:bullseye)

buildcmd() {
    buildah run --network host "${c}" -- "$@"
}

buildah config --workingdir /root "${c}"

buildcmd apt update --quiet=2
buildcmd apt install --yes --quiet=2 git

buildcmd apt install --yes --quiet=2 "${py_deps[@]}"

buildcmd apt install --yes --quiet=2 "${lint_deps[@]}"

buildcmd apt install --yes --quiet=2 "${proj_deps[@]}" "${proj_build_deps[@]}"

for pyver in "${pyversions[@]}"; do
    # shellcheck disable=SC2001
    # strip off any beta or rc suffix to get version directory
    verdir=$(echo "${pyver}" | sed -e 's/^\([[:digit:]]*\.[[:digit:]]*\.[[:digit:]]*\).*$/\1/')
    wget --quiet --output-document - "https://www.python.org/ftp/python/${verdir}/Python-${pyver}.tgz" | tar --extract --gzip
    buildah run --network host --volume "${scriptdir}:/scriptdir" --volume "$(pwd)/Python-${pyver}:/${pyver}" "${c}" -- /scriptdir/pybuild.sh "/${pyver}"
    rm -rf "Python-${pyver}"
done

buildcmd sh -c "rm -rf /usr/local/bin/python3.?m*"
buildcmd sh -c "rm -rf /usr/local/bin/python3.??m*"

buildcmd pip3.10 install hatch
buildcmd mkdir /root/hatch
for env in "${hatchenvs[@]}"; do
    # this looks weird... but it causes Hatch to create the env,
    # install all of the project's dependencies and the project,
    # then runs pip to uninstall the project, leaving the env
    # in place with the dependencies
    #
    # HATCH_ENV_TYPE_VIRTUAL_PATH is used here to force the
    # environments to be created in predictable locations
    case "${env}" in
	ci*)
	    for py in "${cimatrix[@]}"; do
		buildah run --network host --volume "$(realpath "${scriptdir}/.."):/src" --workingdir "/src" "${c}" -- env "HATCH_ENV_TYPE_VIRTUAL_PATH=/root/hatch/${env}.${py}" hatch env create "${env}.${py}"
		buildah run --network host --volume "$(realpath "${scriptdir}/.."):/src" --workingdir "/src" "${c}" -- env "HATCH_ENV_TYPE_VIRTUAL_PATH=/root/hatch/${env}.${py}" hatch -e "${env}.${py}" run pip uninstall --yes "${projname}"
	    done
	;;
	*)
	    buildah run --network host --volume "$(realpath "${scriptdir}/.."):/src" --workingdir "/src" "${c}" -- env "HATCH_ENV_TYPE_VIRTUAL_PATH=/root/hatch/${env}" hatch env create "${env}"
	    buildah run --network host --volume "$(realpath "${scriptdir}/.."):/src" --workingdir "/src" "${c}" -- env "HATCH_ENV_TYPE_VIRTUAL_PATH=/root/hatch/${env}" hatch -e "${env}" run pip uninstall --yes "${projname}"
	;;
    esac
done

buildcmd apt remove --yes --purge "${py_deps[@]}"
buildcmd apt remove --yes --purge "${proj_build_deps[@]}"
buildcmd apt autoremove --yes --purge
buildcmd apt clean autoclean
buildcmd sh -c "rm -rf /var/lib/apt/lists/*"
buildcmd rm -rf /root/.cache

# install reviewdog
# wget "https://github.com/reviewdog/reviewdog/releases/download/v${reviewdog_version}/reviewdog_${reviewdog_version}_Linux_x86_64.tar.gz"
# tar xf "reviewdog_${reviewdog_version}_Linux_x86_64.tar.gz" reviewdog
# buildah copy "${c}" reviewdog /usr/local/bin
# rm "reviewdog_${reviewdog_version}_Linux_x86_64.tar.gz" reviewdog

# shellcheck disable=SC2154 # image_name set in external environment
if buildah images --quiet "${image_name}"; then
    buildah rmi "${image_name}"
fi
buildah commit --squash --rm "${c}" "${image_name}"
