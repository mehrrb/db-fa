# DB-FA: Food & Recipe Management System

A comprehensive Django-based food and recipe management system with REST API support, designed for managing ingredients, recipes, and cost calculations.

> **⚠️ Note**: This project is still under development and not yet complete.

## 🚀 Features

### Core Functionality
- **Category Management**: Organize food items by categories
- **Product Type Management**: Define base products with waste calculations
- **Product Instance Tracking**: Track actual purchases with price and weight
- **Recipe Management**: Create and manage recipes with ingredients
- **Cost Calculation**: Automatic cost calculation including waste factors
- **Profit Analysis**: Calculate profit margins and percentages

### Technical Features
- **Django REST Framework**: Full API support with Swagger documentation
- **Token Authentication**: Secure API access
- **User Management**: Custom user profiles and authentication
- **CSV Import**: Bulk import product types from CSV files
- **Responsive UI**: Bootstrap-based responsive design
- **Internationalization**: Persian (Farsi) language support

## 🛠️ Technology Stack

- **Backend**: Django 5.2.1, Django REST Framework 3.14.0
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript, jQuery, Select2
- **Documentation**: Swagger UI, ReDoc
- **Testing**: Django TestCase (33 tests)
- **Other**: Pandas for data processing
- **Code Quality**: Pre-commit hooks (black, isort, flake8, autoflake)

## 📋 Prerequisites

- Python 3.10+
- PostgreSQL
- pip

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd db-fa
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Database setup**
   ```bash
   python3 manage.py migrate
   python3 manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python3 manage.py runserver
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@localhost:5432/db_fa
STATIC_URL=/static/
MEDIA_URL=/media/
```

### Database Configuration

The system uses PostgreSQL. Make sure to:
1. Create a PostgreSQL database
2. Update the `DATABASE_URL` in your `.env` file
3. Run migrations: `python3 manage.py migrate`

## 📚 API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **API Root**: http://localhost:8000/api/

### Authentication

The API supports token authentication:

```bash
# Get token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# Use token
curl -H "Authorization: Token your_token_here" \
  http://localhost:8000/api/categories/
```

## 🧪 Testing

Run the test suite:

```bash
python3 manage.py test
```

The project includes 33 comprehensive tests covering:
- Model functionality
- Business logic calculations
- API endpoints
- User authentication
- Edge cases and error handling

## 🔧 Code Quality

The project uses pre-commit hooks to ensure code quality:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

**Code Quality Tools:**
- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **autoflake**: Remove unused imports
- **trailing-whitespace**: Remove trailing spaces
- **end-of-file-fixer**: Ensure files end with newline

## 📊 Models Overview

### Core Models
- **Category**: Food categories (e.g., Vegetables, Meat, Dairy)
- **ProductType**: Base product definitions with waste calculations
- **ProductInstance**: Actual purchased products with prices
- **Recipe**: Recipe definitions with cost calculations
- **RecipeItem**: Individual ingredients in recipes

### User Models
- **User**: Extended Django user model
- **Profile**: User profile with additional information

## 🔄 Business Logic

### Waste Calculation
Products have a waste factor that affects cost calculations:
- Waste ratio = waste_percentage / 100
- Waste weight = total_weight × waste_ratio
- Net weight = total_weight - waste_weight

### Cost Calculation
- Base price = (price_per_kilo × total_weight) / 1000
- Waste cost = (price_per_kilo × waste_weight) / 1000
- Total cost = base_price + waste_cost

### Profit Analysis
- Profit = selling_price - total_cost
- Profit percentage = (profit / total_cost) × 100

## 🎯 Usage Examples

### Creating a Recipe
1. Create categories and product types
2. Add product instances with actual prices
3. Create a recipe and add ingredients
4. Set selling price to calculate profit

### CSV Import
1. Prepare CSV file with columns: name, base_weight, waste, unit, category
2. Use admin interface: Admin → Product Types → Import CSV
3. Bulk import product types

## 🚀 Deployment

### Production Settings
1. Set `DEBUG=False` in environment
2. Configure `ALLOWED_HOSTS` properly
3. Set up static file serving
4. Configure database for production
5. Set up proper logging

### Docker (Optional)
```dockerfile
# Add Dockerfile for containerized deployment
FROM python:3.10
# ... Docker configuration
```

## 📈 Performance Considerations

- Database indexing on frequently queried fields
- Pagination for large datasets
- Caching for expensive calculations
- Select_related and prefetch_related for API optimization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the API documentation
2. Review the test cases for usage examples
3. Create an issue in the repository

## 🔄 Changelog

### Version 1.0.0
- Initial release
- Django REST Framework integration
- Complete API documentation
- Comprehensive test suite
- Environment variable configuration
- Persian language support

---

**Made with ❤️ using Django and Django REST Framework**
