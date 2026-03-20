## **Design of Components**

### **Manager View (APIs / Export Jobs)**

#### **Manager Home Page (Dashboard)**

- [ ] Overview of today's appointments  
- [ ] Staff attendance and availability  
- [ ] Low stock inventory alerts  
- [ ] Pending replenishment requests  
- [ ] Quick access to appointments, services, and inventory management

#### **Staff Management**

- [ ] Create staff user  
- [ ] Edit staff member  
- [ ] Delete staff member (only if not assigned to appointments, invoices, or product usage)  
- [ ] Search staff member and view service history and product ordering history

#### **Appointment Management**

- [ ] Create appointment  
- [ ] Edit appointment  
- [ ] Assign / Unassign staff to appointment  
- [ ] Cancel appointment  
- [ ] Track appointment status  
- [ ] View available staff for a selected day

#### **Service Management**

- [ ] Create service with appropriate pricing and estimated duration  
- [ ] Edit service details  
- [ ] Delete service (only if not assigned to appointments, invoices or staff members)  
- [ ] Search and view services or service categories including price, duration, and ratings

#### **Inventory Management**

- [ ] Create product with essential details including product name, category, cost per unit, minimum quantity on hand, and initial stock quantity  
- [ ] Edit product details including description, price, minimum quantity, and supplier details  
- [ ] Delete product (only if stock quantity is zero)  
- [ ] Add product quantity during replenishment  
- [ ] Edit product quantity  
- [ ] View available products with quantities  
- [ ] Automatically add products to replenishment list when stock falls below minimum threshold  
- [ ] Receive notifications when stock quantity drops below minimum quantity on hand  
- [ ] Search for a particular product or product category to view inventory

---

### **Customer View (APIs / Export Jobs)**

#### **Customer Home Page (Dashboard)**

- [ ] Overview of upcoming appointments  
- [ ] Available services with pricing and duration  
- [ ] Reward points and loyalty information  
- [ ] Appointment history

#### **Customer Account**

- [ ] Register account  
- [ ] Login and redirect to Customer dashboard  
- [ ] Logout  
- [ ] Change password

#### **Appointment Management**

- [ ] Book appointment (date, time, optional staff member)  
- [ ] Edit appointment  
- [ ] Cancel appointment  
- [ ] View appointment history  
- [ ] Search appointments by date

#### **Service Information**

- [ ] View services with pricing and duration  
- [ ] Search services

#### **Customer Feedback**

- [ ] View service history (past invoices)  
- [ ] Give feedback and rating  
- [ ] Update number of reviews for services and staff  
- [ ] Calculate cumulative ratings for services and staff

---

### **Staff View (APIs / Export Jobs)**

#### **Staff Home Page (Dashboard)**

- [ ] View today's assigned appointments  
- [ ] Overview of upcoming appointments  
- [ ] View monthly attendance marks

#### **Staff Operations**

- [ ] Login and redirect to Staff dashboard  
- [ ] Logout  
- [ ] Change password  
- [ ] View assigned appointments  
- [ ] Mark attendance  
- [ ] Notify manager if attendance is not marked by a predefined time  
- [ ] Check product availability and quantity  
- [ ] Request products from stock  
- [ ] View staff ratings received from customers

---
