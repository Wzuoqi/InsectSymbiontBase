# InsectSymbiontBase

A comprehensive database for insect symbionts, offering extensive resources including functional records, genomes, metagenomes and research tools to empower scientific discovery and exploration. Based on Django 4.2, PostgreSQL16.1 and TailwindCSS.

## Project Overview

This project aims to collect and provide the most comprehensive functional records, genomic data, amplicon sequencing, and metagenomic sequencing for insect symbionts. The data has been gathered from literature and public databases, providing valuable insights into the complex relationships between insects and their symbiotic microorganisms.

The website is built using **Django 4.2** for the backend, **PostgreSQL 16.1** for database management, and **TailwindCSS** for front-end styling. It also features AI-assisted code generation for various tasks, helping researchers automate parts of their analysis pipeline.

## Features

- **Comprehensive Database**: Includes functional records, genomes, and sequencing data for insect symbionts.
- **AI-assisted Code Generation**: Generate bioinformatics code based on user input for various analyses.
- **Web Interface**: Easy-to-use frontend developed with TailwindCSS.
- **Database Management**: PostgreSQL database ensuring efficient and secure data storage.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/insect-symbiosis-microbiome.git
   ```

2. Install the required Python dependencies:
   ```bash
   cd insect-symbiosis-microbiome
   pip install -r requirements.txt
   ```

3. Set up the PostgreSQL database:
   - Create a PostgreSQL database and user:
     ```bash
     psql -U postgres
     CREATE DATABASE insect_symbiosis;
     CREATE USER your_user WITH PASSWORD 'your_password';
     ALTER ROLE your_user SET client_encoding TO 'utf8';
     ALTER ROLE your_user SET default_transaction_isolation TO 'read committed';
     ALTER ROLE your_user SET timezone TO 'UTC';
     GRANT ALL PRIVILEGES ON DATABASE insect_symbiosis TO your_user;
     ```
   - Update the database settings in `settings.py`.

4. Run migrations to set up the database schema:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the project through your browser at `http://127.0.0.1:8000`.

## Contributing

Contributions are welcome! Please fork this repository, create a branch, and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

# 昆虫共生菌项目

## 项目概述

该项目旨在收集并提供昆虫共生菌的最全面的功能记录、基因组数据、扩增子测序和宏基因组测序数据。这些数据通过文献和公共数据库收集，提供了昆虫与其共生微生物之间复杂关系的宝贵见解。

本网站采用 **Django 4.2** 构建后端，**PostgreSQL 16.1** 作为数据库管理系统，前端使用 **TailwindCSS** 进行样式修饰。同时，项目还提供了AI辅助代码生成功能，帮助研究人员自动化部分分析流程。

## 功能

- **全面的数据库**：包括昆虫共生菌的功能记录、基因组数据及测序数据。
- **AI辅助代码生成**：根据用户输入生成各种生物信息学分析代码。
- **Web界面**：使用TailwindCSS开发的简洁易用前端。
- **数据库管理**：使用PostgreSQL数据库确保数据存储高效且安全。

## 安装

1. 克隆代码库：
   ```bash
   git clone https://github.com/your-repo/insect-symbiosis-microbiome.git
   ```

2. 安装Python依赖：
   ```bash
   cd insect-symbiosis-microbiome
   pip install -r requirements.txt
   ```

3. 设置PostgreSQL数据库：
   - 创建数据库和用户：
     ```bash
     psql -U postgres
     CREATE DATABASE insect_symbiosis;
     CREATE USER your_user WITH PASSWORD 'your_password';
     ALTER ROLE your_user SET client_encoding TO 'utf8';
     ALTER ROLE your_user SET default_transaction_isolation TO 'read committed';
     ALTER ROLE your_user SET timezone TO 'UTC';
     GRANT ALL PRIVILEGES ON DATABASE insect_symbiosis TO your_user;
     ```
   - 在 `settings.py` 中更新数据库设置。

4. 执行迁移以设置数据库模式：
   ```bash
   python manage.py migrate
   ```

5. 启动开发服务器：
   ```bash
   python manage.py runserver
   ```

6. 在浏览器中访问 `http://127.0.0.1:8000` 以查看项目。

## 贡献

欢迎贡献！请 fork 该仓库，创建一个分支，并提交包含您的更改的 pull request。

## 许可

该项目遵循MIT许可协议 - 详见 [LICENSE](LICENSE) 文件。
```

This README provides clear installation instructions and a basic outline of the project's features in both English and Chinese. You can add more details as the project progresses!