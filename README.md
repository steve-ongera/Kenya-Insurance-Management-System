# Kenya Insurance Management System

A comprehensive insurance management system built with Django, specifically designed for the Kenyan insurance market. This system handles policy management, claims processing, customer management, and financial operations with features tailored to Kenyan regulations and payment methods.

## 🚀 Features

### Core Functionality
- **Multi-Product Insurance Management** - Motor, Health, Life, Property, Marine, Aviation, Liability, Travel, and Agriculture insurance
- **Customer Management** - Support for both individual and corporate customers with Kenyan-specific fields
- **Policy Lifecycle Management** - From quotation to policy issuance, renewals, and cancellations
- **Claims Processing** - Complete claims workflow with document management and approval processes
- **Commission Management** - Automated agent commission calculation and tracking
- **Risk Assessment** - Comprehensive risk evaluation tools, especially for motor insurance

### Kenyan Market Specific Features
- **Mobile Money Integration** - M-Pesa payment tracking and receipt management
- **Local Identification Support** - National ID and KRA PIN validation
- **County-Based Organization** - All 47 Kenyan counties supported
- **Regulatory Compliance** - Built-in audit trails and compliance reporting
- **Multi-Branch Operations** - Support for insurance companies with multiple branches across Kenya
- **Reinsurance Management** - Local and international reinsurance contract management

### Financial Management
- **Multiple Payment Methods** - Cash, cheque, bank transfer, mobile money, and card payments
- **Premium Collection** - Flexible payment frequencies (annual, semi-annual, quarterly, monthly)
- **Claims Settlement** - Automated claims payment processing
- **Commission Tracking** - Real-time commission calculation and payment management
- **Financial Reporting** - Comprehensive financial reports and analytics

## 🛠️ Technology Stack

- **Backend**: Django 4.2+
- **Database**: PostgreSQL (recommended) / SQLite (development)
- **Authentication**: Django's built-in authentication system
- **Admin Interface**: Enhanced Django Admin with custom interfaces
- **File Storage**: Django file handling for document management
- **API**: Django REST Framework (optional)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- PostgreSQL 12+ (for production)
- Git

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/kenya-insurance-system.git
cd kenya-insurance-system
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@localhost:5432/insurance_db
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

# File Upload Settings
MEDIA_ROOT=/path/to/media/files
MEDIA_URL=/media/

# Security Settings (Production)
SECURE_SSL_REDIRECT=False
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
```

### 5. Database Setup
```bash
# Create database (PostgreSQL)
createdb insurance_db

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 6. Load Initial Data (Optional)
```bash
# Load Kenyan counties and sample data
python manage.py loaddata fixtures/counties.json
python manage.py loaddata fixtures/insurance_products.json
python manage.py loaddata fixtures/sample_branches.json
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/admin/` to access the admin interface.

## 📁 Project Structure

```
kenya-insurance-system/
├── insurance/
│   ├── models.py          # Core insurance models
│   ├── admin.py           # Admin interface configuration
│   ├── views.py           # Business logic views
│   ├── urls.py            # URL routing
│   ├── forms.py           # Django forms
│   ├── serializers.py     # API serializers (if using DRF)
│   └── migrations/        # Database migrations
├── templates/             # HTML templates
├── static/               # CSS, JavaScript, images
├── media/                # Uploaded files
├── fixtures/             # Initial data files
├── requirements.txt      # Python dependencies
├── manage.py            # Django management script
└── settings/
    ├── base.py          # Base settings
    ├── development.py   # Development settings
    └── production.py    # Production settings
```

## 💼 Usage

### Admin Interface
1. **Dashboard**: Overview of system statistics and quick actions
2. **Customer Management**: Add and manage individual and corporate customers
3. **Policy Management**: Create policies, manage benefits and riders
4. **Claims Processing**: Handle claims from reporting to settlement
5. **Payment Tracking**: Monitor premium payments and claim settlements
6. **Commission Management**: Track and approve agent commissions
7. **Reports**: Generate regulatory and business reports

### Key Workflows

#### Policy Creation
1. Create customer record
2. Generate quotation
3. Convert quotation to policy
4. Set up payment schedule
5. Calculate agent commission

#### Claims Processing
1. Claims reporting
2. Document collection
3. Investigation and assessment
4. Approval/decline decision
5. Settlement processing

#### Payment Processing
1. Premium collection
2. Receipt generation
3. Commission calculation
4. Financial reconciliation

## 🔐 Security Features

- **User Authentication**: Role-based access control
- **Audit Trails**: Complete system activity logging
- **Data Encryption**: Sensitive data protection
- **Session Management**: Secure session handling
- **File Upload Security**: Validated file uploads
- **SQL Injection Protection**: Django ORM protection

## 📊 Reporting

The system includes comprehensive reporting features:

- **Policy Reports**: Active policies, renewals, cancellations
- **Claims Reports**: Claims statistics, settlement ratios
- **Financial Reports**: Premium collection, commission payments
- **Agent Performance**: Individual agent statistics
- **Regulatory Reports**: IRA compliance reports
- **Customer Analytics**: Customer acquisition and retention

## 🔧 Configuration

### System Settings
Configure system parameters through the admin interface:
- Company information
- Tax rates and fees
- Commission structures
- Payment gateway settings
- Email templates
- Report formats

### Insurance Products
Set up insurance products with:
- Product categories and types
- Premium calculation rules
- Commission rates
- Policy terms and conditions
- Coverage limits

## 🚀 Deployment

### Production Deployment (Ubuntu/CentOS)

1. **Install System Dependencies**
```bash
sudo apt update
sudo apt install python3-pip python3-venv postgresql postgresql-contrib nginx
```

2. **Database Setup**
```bash
sudo -u postgres createuser --interactive
sudo -u postgres createdb insurance_production
```

3. **Application Setup**
```bash
git clone https://github.com/yourusername/kenya-insurance-system.git
cd kenya-insurance-system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Configure Production Settings**
```bash
export DJANGO_SETTINGS_MODULE=settings.production
python manage.py collectstatic
python manage.py migrate
```

5. **Set Up Web Server**
Configure Nginx and Gunicorn for production deployment.

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test insurance

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 📝 API Documentation

If using Django REST Framework:
- API endpoints available at `/api/v1/`
- Interactive documentation at `/api/docs/`
- Authentication required for all endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Add tests for new functionality
5. Commit changes (`git commit -am 'Add new feature'`)
6. Push to branch (`git push origin feature/new-feature`)
7. Create Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Write comprehensive tests
- Update documentation
- Use meaningful commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- **Email**: support@yourcompany.com
- **Documentation**: [Wiki](https://github.com/steve-ongera/kenya-insurance-system/wiki)
- **Issues**: [GitHub Issues](https://github.com/steve-ongera/kenya-insurance-system/issues)

## 🔄 Changelog

### Version 1.0.0 (Current)
- Initial release
- Core insurance management features
- Kenyan market adaptations
- Mobile money integration
- Comprehensive admin interface

### Planned Features
- [ ] Mobile application support
- [ ] Advanced analytics dashboard
- [ ] Automated underwriting
- [ ] Integration with external APIs (NTSA, KRA)
- [ ] Multi-language support (English, Swahili)
- [ ] Advanced reporting with charts

## 📚 Documentation

Detailed documentation is available in the `/docs` folder:
- [User Manual](docs/user-manual.md)
- [API Reference](docs/api-reference.md)
- [Deployment Guide](docs/deployment.md)
- [Developer Guide](docs/developer-guide.md)

## 🙏 Acknowledgments

- Insurance Regulatory Authority (IRA) of Kenya for regulatory guidelines
- Django community for the excellent framework
- Contributors and testers

---

**Note**: This system is designed to comply with Kenyan insurance regulations. Ensure compliance with local laws and regulations before deployment in a production environment.