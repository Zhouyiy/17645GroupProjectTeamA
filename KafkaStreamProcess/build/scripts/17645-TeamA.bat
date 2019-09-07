@if "%DEBUG%" == "" @echo off
@rem ##########################################################################
@rem
@rem  17645-TeamA startup script for Windows
@rem
@rem ##########################################################################

@rem Set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" setlocal

set DIRNAME=%~dp0
if "%DIRNAME%" == "" set DIRNAME=.
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%..

@rem Add default JVM options here. You can also use JAVA_OPTS and 17645_TEAM_A_OPTS to pass JVM options to this script.
set DEFAULT_JVM_OPTS=

@rem Find java.exe
if defined JAVA_HOME goto findJavaFromJavaHome

set JAVA_EXE=java.exe
%JAVA_EXE% -version >NUL 2>&1
if "%ERRORLEVEL%" == "0" goto init

echo.
echo ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:findJavaFromJavaHome
set JAVA_HOME=%JAVA_HOME:"=%
set JAVA_EXE=%JAVA_HOME%/bin/java.exe

if exist "%JAVA_EXE%" goto init

echo.
echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME%
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:init
@rem Get command-line arguments, handling Windows variants

if not "%OS%" == "Windows_NT" goto win9xME_args

:win9xME_args
@rem Slurp the command line arguments.
set CMD_LINE_ARGS=
set _SKIP=2

:win9xME_args_slurp
if "x%~1" == "x" goto execute

set CMD_LINE_ARGS=%*

:execute
@rem Setup the command line

set CLASSPATH=%APP_HOME%\lib\17645-TeamA-1.0-SNAPSHOT.jar;%APP_HOME%\lib\kafka_2.12-2.3.0.jar;%APP_HOME%\lib\gson-2.8.5.jar;%APP_HOME%\lib\json-20190722.jar;%APP_HOME%\lib\kafka-clients-2.3.0.jar;%APP_HOME%\lib\jackson-module-scala_2.12-2.9.9.jar;%APP_HOME%\lib\jackson-dataformat-csv-2.9.9.jar;%APP_HOME%\lib\jackson-datatype-jdk8-2.9.9.jar;%APP_HOME%\lib\jackson-module-paranamer-2.9.9.jar;%APP_HOME%\lib\jackson-databind-2.9.9.jar;%APP_HOME%\lib\jopt-simple-5.0.4.jar;%APP_HOME%\lib\metrics-core-2.2.0.jar;%APP_HOME%\lib\scala-logging_2.12-3.9.0.jar;%APP_HOME%\lib\scala-reflect-2.12.8.jar;%APP_HOME%\lib\scala-library-2.12.8.jar;%APP_HOME%\lib\zkclient-0.11.jar;%APP_HOME%\lib\zookeeper-3.4.14.jar;%APP_HOME%\lib\slf4j-api-1.7.26.jar;%APP_HOME%\lib\zstd-jni-1.4.0-1.jar;%APP_HOME%\lib\lz4-java-1.6.0.jar;%APP_HOME%\lib\snappy-java-1.1.7.3.jar;%APP_HOME%\lib\jackson-annotations-2.9.9.jar;%APP_HOME%\lib\jackson-core-2.9.9.jar;%APP_HOME%\lib\spotbugs-annotations-3.1.9.jar;%APP_HOME%\lib\audience-annotations-0.5.0.jar;%APP_HOME%\lib\paranamer-2.8.jar;%APP_HOME%\lib\jsr305-3.0.2.jar

@rem Execute 17645-TeamA
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %17645_TEAM_A_OPTS%  -classpath "%CLASSPATH%" edu.cmu.cs.seai.teama.kafkastreamprocess.MovieLogKafkaReader %CMD_LINE_ARGS%

:end
@rem End local scope for the variables with windows NT shell
if "%ERRORLEVEL%"=="0" goto mainEnd

:fail
rem Set variable 17645_TEAM_A_EXIT_CONSOLE if you need the _script_ return code instead of
rem the _cmd.exe /c_ return code!
if  not "" == "%17645_TEAM_A_EXIT_CONSOLE%" exit 1
exit /b 1

:mainEnd
if "%OS%"=="Windows_NT" endlocal

:omega
