from mcp.server.fastmcp import FastMCP
import pymysql.cursors

# ========================================
# Configuration: MySQL Connection Details
# ========================================
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Shashi@2005!',
    'database': 'leave_request',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    """Establish and return a new MySQL connection."""
    return pymysql.connect(**MYSQL_CONFIG)


# ============================
# Initialize FastMCP Server
# ============================
mcp = FastMCP("MySQLLeaveTracker")


# ============================================
# Tool: Submit a Leave Request
# ============================================
@mcp.tool()
def submit_leave(student_id: str, date: str, reason: str) -> str:
    """
    Submit a leave request for a student.

    Args:
        student_id (str): ID of the student.
        date (str): Date of the leave (YYYY-MM-DD).
        reason (str): Reason for the leave.

    Returns:
        str: Result message.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check for existing request
        cursor.execute("SELECT 1 FROM leave_request WHERE student_id = %s AND date = %s", (student_id, date))
        if cursor.fetchone():
            return f"⚠️ Leave already submitted for {date} by {student_id}."

        # Insert new leave request
        cursor.execute(
            "INSERT INTO leave_request (student_id, date, reason, status) VALUES (%s, %s, %s, %s)",
            (student_id, date, reason, "pending")
        )
        conn.commit()
        return f"✅ Leave submitted for {student_id} on {date}."
    except Exception as e:
        conn.rollback()
        return f"❌ Error submitting leave: {e}"
    finally:
        conn.close()


# ============================================
# Tool: Update Leave Request Status
# ============================================
@mcp.tool()
def update_status(student_id: str, date: str, new_status: str) -> str:
    """
    Update the status of a leave request.

    Args:
        student_id (str): Student ID.
        date (str): Leave date.
        new_status (str): New status (e.g., 'approved', 'rejected', 'pending').

    Returns:
        str: Status update message.
    """
    if new_status not in {"pending", "approved", "rejected"}:
        return "❌ Invalid status. Use one of: pending, approved, rejected."

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE leave_request SET status = %s WHERE student_id = %s AND date = %s",
            (new_status, student_id, date)
        )
        conn.commit()
        if cursor.rowcount > 0:
            return f"✅ Leave on {date} for {student_id} marked as '{new_status}'."
        else:
            return f"⚠️ No leave request found for {student_id} on {date}."
    except Exception as e:
        conn.rollback()
        return f"❌ Error updating status: {e}"
    finally:
        conn.close()


# ============================================
# Tool: Retrieve Leave History
# ============================================
@mcp.tool()
def leave_history(student_id: str) -> str:
    """
    Retrieve the leave history of a student.

    Args:
        student_id (str): Student ID.

    Returns:
        str: Leave history in tabular format.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT student_id, date, reason, status FROM leave_request WHERE student_id = %s ORDER BY date DESC",
            (student_id,)
        )
        rows = cursor.fetchall()
        if not rows:
            return "📭 No leave history found."

        # Format as CSV-like table
        header = "student_id, date, reason, status"
        formatted_rows = [header] + [", ".join(str(val) for val in row.values()) for row in rows[:10]]
        return "\n".join(formatted_rows)
    except Exception as e:
        return f"❌ Error fetching history: {e}"
    finally:
        conn.close()


# ============================================
# Tool: List Students
# ============================================
@mcp.tool()
def list_students(limit: int = 100, offset: int = 0) -> str:
    """
    List students from the 'students' table.

    Args:
        limit (int): Number of records to fetch.
        offset (int): Offset for pagination.

    Returns:
        str: List of students.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT student_id, student_name FROM students ORDER BY student_name LIMIT %s OFFSET %s",
            (limit, offset)
        )
        rows = cursor.fetchall()
        if not rows:
            return "📭 No students found."

        header = "student_id, student_name"
        formatted = [header] + [", ".join(str(val) for val in row.values()) for row in rows]
        return "\n".join(formatted)
    except Exception as e:
        return f"❌ Error listing students: {e}"
    finally:
        conn.close()


# ============================================
# Resource: Greeting
# ============================================
@mcp.resource("greeting://{name}")
def greet(name: str) -> str:
    """
    Return a greeting message for the user.
    
    Args:
        name (str): User's name.

    Returns:
        str: Personalized greeting.
    """
    return f"👋 Hello, {name}! I’m here to help manage student leave requests in the MySQL database."


# ============================================
# Start MCP Server
# ============================================
if __name__ == "__main__":
    mcp.run()
