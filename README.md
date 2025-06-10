# Mcp-Claude-Integration

## MySQL Leave Tracker

This project implements a MySQL-based leave request management system using the FastMCP framework. It provides tools to:

*   Submit leave requests for students.
*   Update the status of existing leave requests (pending, approved, rejected).
*   Retrieve the leave history for a specific student.
*   List all registered students.

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/SHASHIKIRAN-S/Mcp-Claude-Integration.git
    cd Mcp-Claude-Integration
    ```

2.  **MySQL Database Configuration:**
    Ensure you have a MySQL server running. Create a database named `leave_request` and a `leave_request` table, and a `students` table as defined in `main.py`. Update the `MYSQL_CONFIG` in `main.py` with your database credentials.

    Example SQL for `leave_request` table:
    ```sql
    CREATE TABLE leave_request (
        student_id VARCHAR(255) NOT NULL,
        date DATE NOT NULL,
        reason TEXT,
        status VARCHAR(50) DEFAULT 'pending',
        PRIMARY KEY (student_id, date)
    );
    ```

    Example SQL for `students` table:
    ```sql
    CREATE TABLE students (
        student_id VARCHAR(255) NOT NULL PRIMARY KEY,
        student_name VARCHAR(255) NOT NULL
    );
    ```

3.  **Install Dependencies:**
    It looks like `uv` and `pyproject.toml` are used for dependency management. You can use `uv` to install the dependencies:
    ```bash
    uv sync
    ```
    If `uv` is not installed, you can install it using `pip`:
    ```bash
    pip install uv
    ```

### Usage

To start the MCP server:

```bash
python main.py
```

Once the server is running, you can interact with the defined tools (e.g., `submit_leave`, `update_status`, `leave_history`, `list_students`) via your FastMCP client.

Example:

```python
# Assuming you have a FastMCP client connected to the server
# from mcp.client.fastmcp_client import FastMCPClient
# client = FastMCPClient("http://localhost:8000") # Replace with your server address

# client.submit_leave(student_id="S123", date="2024-07-20", reason="Fever")
# client.leave_history(student_id="S123")
```