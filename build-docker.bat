@echo off
REM Build and test Docker image for Language Mentor (Windows)

setlocal enabledelayedexpansion

echo =========================================
echo Language Mentor - Docker Build Script
echo =========================================

REM Configuration
set IMAGE_NAME=language-mentor
if "%1"=="" (
    set TAG=latest
) else (
    set TAG=%1
)
set FULL_IMAGE_NAME=%IMAGE_NAME%:%TAG%

echo.
echo Building image: %FULL_IMAGE_NAME%
echo.

REM Build the image
echo Step 1: Building Docker image...
docker build -t %FULL_IMAGE_NAME% .

if errorlevel 1 (
    echo Error: Docker build failed!
    exit /b 1
)

echo.
echo Step 2: Image built successfully!
docker images | findstr %IMAGE_NAME%

REM Optional: Run tests in container
echo.
set /p RUN_TESTS="Run tests in container? (y/n) "
if /i "%RUN_TESTS%"=="y" (
    echo Step 3: Running tests in container...
    docker build --target testing -t %IMAGE_NAME%:test .
    echo Tests completed!
)

REM Optional: Start the container
echo.
set /p START_CONTAINER="Start the container? (y/n) "
if /i "%START_CONTAINER%"=="y" (
    echo Step 4: Starting container...

    REM Check if .env file exists
    if not exist .env (
        echo Warning: .env file not found. Copying from .env.example...
        copy .env.example .env
        echo Please edit .env with your Azure OpenAI credentials before the container can work properly.
    )

    docker run -d ^
        --name language-mentor-app ^
        -p 7860:7860 ^
        --env-file .env ^
        -v "%cd%\logs:/app/logs" ^
        %FULL_IMAGE_NAME%

    echo.
    echo Container started successfully!
    echo Access the application at: http://localhost:7860
    echo.
    echo View logs: docker logs -f language-mentor-app
    echo Stop container: docker stop language-mentor-app
    echo Remove container: docker rm language-mentor-app
)

echo.
echo =========================================
echo Build completed successfully!
echo =========================================

endlocal

