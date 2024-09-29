PACKAGE_VERSION=0.2

echo $PACKAGE_VERSION

export IMAGE_URL=registry.cn-chengdu.aliyuncs.com/py_dc/crawler

if [ $? == 0 ]; then
  echo "/-------------------- docker build --------------------/"
  # docker build --cache-from "${IMAGE_URL}:0.0.1" -t "${IMAGE_URL}:0.0.1" -t "${IMAGE_URL}:daily-$PACKAGE_VERSION" .
  docker build -f ./docker/Dockerfile.api -t "${IMAGE_URL}:0.0.1" -t "${IMAGE_URL}:daily-$PACKAGE_VERSION" .
fi

if [ $? == 0 ]; then
  echo "/-------------------- docker push --------------------/"
  docker push "${IMAGE_URL}:daily-$PACKAGE_VERSION"
fi
