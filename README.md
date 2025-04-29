Containerized-Chronicles-An-authenticated-blogging-platform

**Project Overview**  
Containerized Chronicles is an authenticated blogging platform developed using Django. It allows users to register either as blog readers or content creators (Admins), while a Super Admin oversees the platform. The system ensures secure access control and role-based permissions for different users.

**Features**  
- Role-Based Authentication  
  - Reader Users: Can register, log in, and read published blogs.  
  - Admin Users: Can register, log in, and create/manage their own blogs.  
  - Super Admin: Full control to manage users, blogs, comments, and administrative settings via the Django admin panel.  
- Blog Management  
  - Admins can create, update, and delete their own blog posts.  
  - Readers can browse and view blog content.  
  - Super Admin can oversee all activities on the platform.  
- Secure Login System  
- Simple and Responsive Interface  

**Technologies Used**
- Python  
- Django    
- HTML & CSS (Template rendering)  
- Bootstrap (for styling)  
- Django Admin (for Super Admin management)  

Key Modules  
- User Authentication & Role Assignment  
- Blog CRUD Operations  
- Access Control based on User Role  
- Admin Panel for Super Admin  

**How to Run**

cd containerized-chronicles  

Set Up Virtual Environment  
```bash
python -m venv venv
```
```bash
source venv/bin/activate
```  

Install Dependencies  
```bash
pip install -r requirements.txt  
```

Apply Migrations and Create Superuser  
```bash
python manage.py makemigrations
python manage.py migrate    
```

Create Superuser:
```bash
python manage.py createsuperuser
```

Run the Server  
```bash
python manage.py runserver  
```
**Future Improvements**  
- Add commenting system for blogs  
- Rich text editor for blog content  
- Email notifications for user activity  
- Blog categories and search functionality  
- REST API integration for mobile support  

**Contributors**  
- Muniraju B R  
- Nithish C  
- Gunashree H M  

**Acknowledgments**  
Thanks to the team and mentors who guided the development of this project.
