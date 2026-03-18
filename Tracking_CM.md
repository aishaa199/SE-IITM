## **Design of Components**

### **Public Home Page (Before Login)**

- [ ] Overview of the beauty parlor and services offered  
- [ ] List of popular or featured services  
- [ ] Staff highlights and customer ratings  
- [ ] Customer testimonials or reviews  
- [ ] Promotions, offers, or loyalty program information  
- [ ] Quick navigation to Register / Login  
- [ ] Contact information and location details

---

### **Owner View (APIs / Export Jobs)**

#### **Owner Home Page (Dashboard)**

- [ ] Overview of business performance metrics  
- [ ] Summary of revenue trends and service demand  
- [ ] Staff productivity overview  
- [ ] Access to monthly reports

#### **Owner Operations**

- [ ] Create Manager user  
- [ ] Login and redirect to Owner dashboard  
- [ ] Logout  
- [ ] Change password  
- [ ] View monthly reports for productivity, service demand, and revenue trends

---

### **Manager View (APIs / Export Jobs)**

- [ ] Login and redirect to Manager’s dashboard  
- [ ] Logout  
- [ ] Change password

#### 

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

#### **Customer Management**

- [ ] Create customer  
- [ ] Edit customer details  
- [ ] View customer preferences and history  
- [ ] Search for a particular customer to view appointments and invoices  
- [ ] Automatically update number of visits of customer  
- [ ] Update customer type ( normal → VIP)  
- [ ] Update customer preferences

#### **Billing and Financial Records**

- [ ] Create invoice  
- [ ] Save details for financial reporting

#### **Reports**

- [ ] Generate daily revenue report  
- [ ] Generate replenishment report  
- [ ] Generate stock usage report on demand showing products claimed by individual staff members within a selected date range

#### **Rewards &  Notifications**

- [ ] Calculate reward points and expiry dates based on predefined criteria  
- [ ] Send notifications to customers regarding reward points  
- [ ] Send email with replenishment requisition to the wholesaler  
- [ ] View ratings of products and staff

---

### **Staff View (APIs / Export Jobs)**

#### **Staff Home Page (Dashboard)**

- [ ] View today's assigned appointments  
- [ ] Overview of upcoming services  
- [ ] Notifications from manager

#### **Staff Operations**

- [ ] Login and redirect to Staff dashboard  
- [ ] Logout  
- [ ] Change password  
- [ ] View assigned appointments  
- [ ] Mark attendance  
- [ ] Notify manager if attendance is not marked by a predefined time  
- [ ] Check product availability and quantity  
- [ ] Request products from stock  
- [ ] Search and view products for availability  
- [ ] Search customers to view service history and preferences  
- [ ] View ratings of products and staff

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