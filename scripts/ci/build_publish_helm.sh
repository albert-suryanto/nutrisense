#! /bin/sh

SHA="$(echo "${GITHUB_SHA}" | head -c 6)"
BRANCH="$(echo "${GITHUB_BRANCH}" | sed 's/[._-]*$//')"
IMAGE_VERSION="${SHA}-${BRANCH}"

HELM_VERSION=$1

if [ -z "$1" ]; then
  HELM_VERSION="v0.0.0-${IMAGE_VERSION}"
fi

cd ./infra/chart || exit

helm dependency update
helm package . -u --version "${HELM_VERSION}" --app-version "${IMAGE_VERSION}" -d ./uploads
helm plugin install https://github.com/chartmuseum/helm-push

for filename in ./uploads/*.tgz; do
  helm cm-push --username="${HARBOR_USER}" --password="${HARBOR_PASSWORD}" "$filename" "https://${DOMAIN}/${HARBOR_CHART_REF}"
done

rm -rf ./uploads
