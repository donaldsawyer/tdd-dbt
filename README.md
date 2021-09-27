# Overview
This demo aims to provide a set of examples and frameworks for doing test-driven data engineering (TDDE).

## Prerequisites

To run this demo, the following applications must be installed.

|Tool|Mac Demo Version|Windows Version|
|--|--|--|
|Python|[Python 3.8.2](https://www.python.org/downloads/macos/)||
|Docker|[docker desktop](https://www.cprime.com/resources/blog/docker-on-mac-with-homebrew-a-step-by-step-tutorial/) (really only need docker)<br><ul><li>docker desktop 3.3.3</li><li>docker 20.10.6</li></ul>||
|dbt|[dbt 0.20.1_1](https://docs.getdbt.com/dbt-cli/installation)||
|dbt-sqlserver plugin|0.19.0<br>*NOTE: 0.20.0 did not install properly, so downgraded to 0.19.0*||
|dbt-snowflake plugin|0.20.1||

## Helpful References
Below are some references that have been used to learn more about the activities in this repo. It is recommended to read them for yourself as you start/continue the `dbt` journey.

* DBT Slack Channel [Join Here](https://community.getdbt.com/)
* Building a Scalable Analytics Architecture with Airflow and dbt
 * [Part 1](https://www.astronomer.io/blog/airflow-dbt-1)
 * [Part 2](https://www.astronomer.io/blog/airflow-dbt-2)
* [Data Mock Tool Plugin](https://github.com/mjirv/dbt-datamocktool)
* [GitLab dbt Guide](https://about.gitlab.com/handbook/business-technology/data-team/platform/dbt-guide/)
* [dbt coves](https://pypi.org/project/dbt-coves/)
* Flight [data dictionary on BTS.gov](https://www.transtats.bts.gov/DL_SelectFields.asp?gnoyr_VQ=FGK&QO_fu146_anzr=b0-gvzr)

# Mac Setup


## Docker Setup

**Pull the Docker Image**
Pull the docker image you'd like to use. The [MS SQL Server dockerhub page](https://hub.docker.com/_/microsoft-mssql-server) is a good resource.

*COMMAND:*
```
docker pull mcr.microsoft.com/mssql/server:2019-latest
```

**Run the Docker Image**
Run the docker image to start a container that has MS SQL Server running within it.

*COMMAND:*
```
docker run -d --name sql_server -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=ITsC0mpl1cat3d' -p 1433:1433 mcr.microsoft.com/mssql/server:2019-latest
```

### Docker Verification

There are multiple ways to verify the image, two are:
1. Connect a SQL Prompt within the container (via docker tools)
1. Connect to the SQL instance using a connection (similar to normal connection)

#### Verification Using Docker Tools
Using docker tools, you can open a command prompt inside the SQL Server docker container. The container has the `mssql-tools` pre-installed.

The command below will open a `sqlcmd` prompt inside the docker container, using the username and password provided.
```
docker exec -it sql_server /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P ITsC0mpl1cat3d
```
Verify you have a running instance with a simple `select` query (*don't forget the `go`*):
```
1> select @@version
2> go
```

The response should look similar to the response below:
```
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Microsoft SQL Server 2019 (RTM-CU12) (KB5004524) - 15.0.4153.1 (X64)
	Jul 19 2021 15:37:34
	Copyright (C) 2019 Microsoft Corporation
	Developer Edition (64-bit) on Linux (Ubuntu 20.04.2 LTS) <X64>

(1 rows affected)
```

#### Verification with sqlcmd on Your Machine
Setting up your Mac to use `sqlcmd` requires a couple of additional steps:
1. Install the SQL Server drivers and sql tools
1. Connect to SQL Server using the ODBC connection


First, install the MSSQL ODBC Drivers AND MSSQL tools using the code in [this reference](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver15) (code below).
```
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
HOMEBREW_NO_ENV_FILTERING=1 ACCEPT_EULA=Y brew install msodbcsql17 mssql-tools
```

Next, verify you can connect to the SQL Server Docker instance and run the `select @@version`, and your response should be the same as with the docker command verification above:
```
% sqlcmd -S localhost -U sa -P ITsC0mpl1cat3d
1> select @@version
2> go
```

*NOTE: There are alternate ways to connect using the ODBC driver. This may help if you need other means.*
* Connect using localhost + port `sqlcmd -S localhost,1433 -U sa -P ITsC0mpl1cat3d`
* Connect using localhost IP + port `sqlcmd -S 127.0.0.1,1433 -U sa -P ITsC0mpl1cat3d`
* Connect using configured IP + port `sqlcmd -S 0.0.0.0,1433 -U sa -P ITsC0mpl1cat3d`

### Stopping/Starting SQL Server
If you want to take the SQL Server container down, just run the stop command:
```
docker stop sql_server
```

Next time you need the container:
```
docker start sql_server
```
