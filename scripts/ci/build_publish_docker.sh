#! /bin/sh

# check for necessary env vars
[ "${DOMAIN}" = '' ] && echo "❌ 'DOMAIN' env var not set" && exit 1
[ "${GITHUB_REPO_REF}" = '' ] && echo "❌ 'GITHUB_REPO_REF' env var not set" && exit 1
[ "${GITHUB_SHA}" = '' ] && echo "❌ 'GITHUB_SHA' env var not set" && exit 1
[ "${GITHUB_BRANCH}" = '' ] && echo "❌ 'GITHUB_BRANCH' env var not set" && exit 1

[ "${CI_DOCKER_IMAGE}" = '' ] && echo "❌ 'CI_DOCKER_IMAGE' env var not set" && exit 1
[ "${CI_DOCKER_CONTEXT}" = '' ] && echo "❌ 'CI_DOCKER_CONTEXT' env var not set" && exit 1
[ "${CI_DOCKERFILE}" = '' ] && echo "❌ 'CI_DOCKERFILE' env var not set" && exit 1

[ "${DOCKER_PASSWORD}" = '' ] && echo "❌ 'DOCKER_PASSWORD' env var not set" && exit 1
[ "${DOCKER_USER}" = '' ] && echo "❌ 'DOCKER_USER' env var not set" && exit 1

[ "${AWS_KEY_ID}" = '' ] && echo "❌ 'AWS_KEY_ID' env var not set" && exit 1
[ "${AWS_KEY_SECRET}" = '' ] && echo "❌ 'AWS_KEY_SECRET' env var not set" && exit 1
[ "${AWS_BUCKET}" = '' ] && echo "❌ 'AWS_KEY_SECRET' env var not set" && exit 1
[ "${AWS_REGION}" = '' ] && echo "❌ 'AWS_KEY_SECRET' env var not set" && exit 1

[ "${LATEST_BRANCH}" = '' ] && echo "❌ 'LATEST_BRANCH' env var not set" && exit 1

set -eu

onExit() {
  rc="$?" # The $? is a special variable in Bash that holds the exit status of the previous command. A zero exit status (0) indicates success, while a non-zero exit status indicates an error or failure.
  if [ "$rc" = '0' ]; then
    echo "✅ Successfully built and run images"
  else
    echo "❌ Failed to run Docker image"
  fi
}

# The trap command is used to catch signals and execute a specified command or function when a signal is received. In this case, the trap command is set to catch the EXIT signal, which is sent when the shell is about to exit or when a command fails
trap onExit EXIT

# Login to GitHub Registry
echo "🔐 Logging into docker registry..."
echo "${DOCKER_PASSWORD}" | docker login "${DOMAIN}" -u "${DOCKER_USER}" --password-stdin
echo "✅ Successfully logged into docker registry!"

echo "📝 Generating Image tags..."

# Obtain image
IMAGE_ID="${DOMAIN}/${GITHUB_REPO_REF}/$(echo "${CI_DOCKER_IMAGE}" | sed 's/[._-]*$//')" # sed 's/[._-]*$//' is a sed command that uses a regular expression to remove the trailing substring of the input string. The regular expression [._-]* matches any sequence of characters that are either an underscore, a dot, or a hyphen. The s/.../\$1/ part of the expression replaces the matched substring with an empty string, effectively removing it from the input string
IMAGE_ID=$(echo "${IMAGE_ID}" | tr '[:upper:]' '[:lower:]')                              # convert to lower case. tr command translates, deletes, and squeezes characters from the standard input and writes the result to the standard output. It is often used for character manipulation, such as removing repeated characters, converting uppercase to lowercase, and basic character replacing and removing.

# obtaining the version
SHA="$(echo "${GITHUB_SHA}" | head -c 6)"
BRANCH="$(echo "${GITHUB_BRANCH}" | sed 's/[._-]*$//')"
IMAGE_VERSION="${SHA}-${BRANCH}"

# Generate image references
COMMIT_IMAGE_REF="${IMAGE_ID}:${IMAGE_VERSION}"
BRANCH_IMAGE_REF="${IMAGE_ID}:${BRANCH}"
LATEST_IMAGE_REF="${IMAGE_ID}:latest"

# Generate cache references
CACHE_COMMIT="${IMAGE_ID}/${SHA}-${BRANCH}"
CACHE_BRANCH="${IMAGE_ID}/${BRANCH}"
CACHE_LATEST="${IMAGE_ID}/latest"

echo "  ✅ Commit Image Ref: ${COMMIT_IMAGE_REF}"
echo "  ✅ Branch Image Ref: ${BRANCH_IMAGE_REF}"
echo "  ✅ Latest Image Ref: ${LATEST_IMAGE_REF}"
echo ""
echo "  ✅ Commit Cache: ${CACHE_COMMIT}"
echo "  ✅ Branch Cache: ${CACHE_BRANCH}"
echo "  ✅ Latest Cache: ${CACHE_LATEST}"

# build image
export AWS_ACCESS_KEY_ID="${AWS_KEY_ID}"
export AWS_SECRET_ACCESS_KEY="${AWS_KEY_SECRET}"

echo "🔨 Building Dockerfile..."

# buildx extends the docker build command with the full support of the features provided by Moby BuildKit builder toolkit. It allows you to create scoped builder instances and build against multiple nodes concurrently
docker buildx build \
  "${CI_DOCKER_CONTEXT}" \
  -f "${CI_DOCKERFILE}" \
  --platform=linux/arm64 \
  --push \
  --cache-from "type=s3,region=${AWS_REGION},bucket=${AWS_BUCKET},name=${CACHE_COMMIT}" \
  --cache-from "type=s3,region=${AWS_REGION},bucket=${AWS_BUCKET},name=${CACHE_BRANCH}" \
  --cache-from "type=s3,region=${AWS_REGION},bucket=${AWS_BUCKET},name=${CACHE_LATEST}" \
  --cache-to "type=s3,region=${AWS_REGION},bucket=${AWS_BUCKET},ref=${CACHE_COMMIT};${CACHE_BRANCH};${CACHE_LATEST},mode=max" \
  -t "${COMMIT_IMAGE_REF}" \
  -t "${BRANCH_IMAGE_REF}"

echo "✅ Pushed branch image!"

# push latest
if [ "$BRANCH" = "$LATEST_BRANCH" ]; then
  echo "🔎 Detected branch is '${BRANCH}', pulling currently built image..."
  docker pull --platform linux/arm64 "${COMMIT_IMAGE_REF}"
  echo "✅Pulled image ${COMMIT_IMAGE_REF}"
  docker tag "${COMMIT_IMAGE_REF}" "${LATEST_IMAGE_REF}"
  docker push "${LATEST_IMAGE_REF}"
  echo "✅ Pushed branch as latest image!"
fi
