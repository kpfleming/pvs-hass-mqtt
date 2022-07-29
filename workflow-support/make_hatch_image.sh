#!/usr/bin/env bash

set -ex

projname="pvs-hass-mqtt"

scriptdir=$(realpath "$(dirname "${BASH_SOURCE[0]}")")

lintdeps=(shellcheck)
pydeps=(build-essential libreadline-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev)
proj_deps=(libsystemd)
proj_build_deps=(pkg-config libsystemd-dev)

pyversions=(3.8.13 3.9.13 3.10.5 3.11.0b5)

hatchenvs=(lint lint-action ci ci-systemd)

c=$(buildah from debian:bullseye)

buildcmd() {
    buildah run --network host "${c}" -- "$@"
}

buildah config --workingdir /root "${c}"

buildcmd apt update --quiet=2
buildcmd apt install --yes --quiet=2 git

buildcmd apt install --yes --quiet=2 "${pydeps[@]}"

buildcmd apt install --yes --quiet=2 "${lintdeps[@]}"

buildcmd apt install --yes --quiet=2 "${projdeps[@]}" "${proj_build_deps[@]}"

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
for env in "${hatchenvs[@]}"; do
    # this looks weird... but it causes Hatch to create the env,
    # install all of the project's dependencies and the project,
    # then runs pip to uninstall the project, leaving the env
    # in place with the dependencies
    #
    # the bizarre volume-mount path matches the path that
    # actions/checkout@v3 will place the checkout into;
    # this is needed because Hatch uses the path
    # as part of the hash calculation for the name
    # of the directory to hold the environments
    buildah run --network host --volume "$(realpath "${scriptdir}/.."):/__w/${projname}/${projname}" --workingdir "/__w/${projname}/${projname}" "${c}" -- hatch --data-dir /root/hatch -e "${env}" run pip uninstall --yes "${projname}"
done

buildcmd apt remove --yes --purge "${pydeps[@]}"
buildcmd apt remove --yes --purge "${proj_build_deps[@]}"
buildcmd apt autoremove --yes --purge
buildcmd apt clean autoclean
buildcmd sh -c "rm -rf /var/lib/apt/lists/*"
buildcmd rm -rf /root/.cache

# shellcheck disable=SC2154 # image_name set in external environment
if buildah images --quiet "${image_name}"; then
    buildah rmi "${image_name}"
fi
buildah commit --squash --rm "${c}" "${image_name}"
