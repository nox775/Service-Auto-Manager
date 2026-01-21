# 🚗 Service Auto Manager

### Project Description

**Service Auto Manager** is a comprehensive desktop application designed to digitize the workflow of an automotive repair shop. The application replaces paper-based records with a robust relational database, enabling efficient management of clients, the vehicle fleet, parts inventory, and the invoicing process.

The project was developed to demonstrate advanced proficiency in **Python** programming and **MySQL** database design, prioritizing data integrity, complex SQL queries, and a modern graphical user interface.

---

### 🛠️ Technologies Used

* **Language:** Python 3.10+
* **User Interface (GUI):** `tkinter` utilizing the `ttkbootstrap` library (for a modern dark-mode theme).
* **Database:** MySQL (Relational architecture, 3NF normalized).
* **Key Libraries:**
* `mysql-connector-python`: Database connectivity and manipulation.
* `atplotlib`: Generation of charts and visual statistics.
* `reportlab`: Automated generation of PDF invoices.



---

### ✨ Key Features

**1. Operational Management (CRUD)**

* **Client & Vehicle Registry:** Add and modify data regarding clients and their vehicles, including validation for unique fields (e.g., VIN, Phone Number).
* **HR & Services:** Administration of the mechanics team and the service catalog (labor) with standardized hourly rates.

**2. Repair Workflow**

* **Repair Order System (Devize):** Creation of repair files, assignment of mechanics, and real-time status tracking (e.g., "In Progress", "Waiting for Parts").
* **Inventory Management:** Automatic deduction of parts stock at the moment they are added to a repair order.

**3. Reporting & Business Intelligence**

* **Automated Invoicing:** Instant generation of fiscal invoices (PDF) based on the parts and labor recorded in the repair order, with automatic VAT calculation.
* **Statistical Dashboard:** Graphical visualization of shop performance (monthly revenue, top mechanics, repair types).
* **Advanced Modules (Complex SQL):**
* **CRM:** Identification of inactive clients (who haven't returned in the last 6 months) using subqueries.
* **Audit:** Detection of "dead stock" (unsold parts) and efficiency discrepancies.



---

### 🗄️ Database Structure

The database is relationally structured to avoid redundancy and ensure consistency.

* **1:N Relationships:** A client owns multiple vehicles; a vehicle has a history of multiple repair orders.
* **N:M Relationships:** A repair order includes multiple parts and services performed by multiple mechanics (managed via the associative tables `MANOPERA` and `COMANDA_PIESE`).
