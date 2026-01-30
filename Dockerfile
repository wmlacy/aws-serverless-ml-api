# Dockerfile
FROM public.ecr.aws/lambda/python:3.11

# Install deps
COPY app/requirements.txt  ./requirements.txt
RUN python3.11 -m pip install --only-binary :all: -r requirements.txt -t "${LAMBDA_TASK_ROOT}"

# Copy training script and train model inside container
COPY train.py /tmp/train.py
WORKDIR ${LAMBDA_TASK_ROOT}
RUN mkdir -p app && PYTHONPATH="${LAMBDA_TASK_ROOT}" python3.11 /tmp/train.py && mv app/model.pkl ${LAMBDA_TASK_ROOT}/model.pkl && rm -rf app

# Copy handler code
COPY app/handler.py ${LAMBDA_TASK_ROOT}/

# Lambda handler entrypoint: file.function
CMD ["handler.lambda_handler"]
