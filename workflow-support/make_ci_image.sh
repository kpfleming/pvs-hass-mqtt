#!/usr/bin/env bash

set -ex

projname="pvs-hass-mqtt"

scriptdir=$(realpath "$(dirname "${BASH_SOURCE[0]}")")

lint_deps=(shellcheck)
proj_deps=(libsystemd0 libsqlite3-0)
proj_build_deps=(build-essential libc6-dev pkg-config libsystemd-dev)

hatchenvs=(lint ci ci-systemd)
cimatrix=(py3.8 py3.9 py3.10 py3.11)

c=$(buildah from quay.io/km6g-ci-images/python:bullseye-main)

buildcmd() {
    buildah run --network host "${c}" -- "$@"
}

buildcmd apt update --quiet=2
buildcmd apt install --yes --quiet=2 git
buildcmd apt install --yes --quiet=2 "${lint_deps[@]}" "${proj_deps[@]}" "${proj_build_deps[@]}"

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
