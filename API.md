# Obesity Prediction API Documentation

## Overview

The Obesity Prediction API provides endpoints for predicting obesity risk levels based on health and lifestyle factors.

## Base URL

- Development: `http://localhost:5000`
- Production: `https://your-domain.com`

## Endpoints

### 1. Home Page

**GET** `/`

Returns the main input form for obesity prediction.

**Response:**
- Content-Type: `text/html`
- Status: `200 OK`

### 2. Prediction Endpoint

**POST** `/predict`

Predicts obesity risk level based on submitted form data.

**Request Body:**
Form data with the following fields:

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| gender | string | Gender (Male/Female) | Yes |
| age | number | Age in years | Yes |
| height | number | Height in meters | Yes |
| weight | number | Weight in kilograms | Yes |
| family_history_with_overweight | string | Family history (yes/no) | Yes |
| favc | string | Frequent high caloric food (yes/no) | Yes |
| fcvc | number | Frequency of vegetables consumption | Yes |
| ncp | number | Number of main meals | Yes |
| caec | string | Food between meals (no/Sometimes/Frequently/Always) | Yes |
| smoke | string | Smoking status (yes/no) | Yes |
| ch2o | number | Water consumption per day | Yes |
| scc | string | Calories monitoring (yes/no) | Yes |
| faf | number | Physical activity frequency | Yes |
| tue | number | Technology usage time | Yes |
| calc | string | Alcohol consumption (no/Sometimes/Frequently/Always) | Yes |
| mtrans | string | Transportation mode | Yes |

**Response:**
- Content-Type: `text/html`
- Status: `200 OK` (success) or `400 Bad Request` (error)

**Success Response:**
```html
<html>
  <body>
    <div>
      <h2>Prediction Result</h2>
      <p>Your predicted category: <strong>Normal Weight</strong></p>
      <a href="/">Submit another response</a>
    </div>
  </body>
</html>
```

**Error Response:**
```html
<html>
  <body>
    <div>
      <h2>Error</h2>
      <p>An error occurred: [error message]</p>
      <a href="/">Try again</a>
    </div>
  </body>
</html>
```

## Prediction Categories

The API returns one of the following obesity categories:

1. **Insufficient Weight** - BMI < 18.5
2. **Normal Weight** - BMI 18.5-24.9
3. **Overweight Level I** - BMI 25.0-29.9
4. **Overweight Level II** - BMI 30.0-34.9
5. **Obesity Type I** - BMI 35.0-39.9
6. **Obesity Type II** - BMI 40.0-44.9
7. **Obesity Type III** - BMI ≥ 45.0

## Example Usage

### Using cURL

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "gender=Male&age=25&height=1.75&weight=70&family_history_with_overweight=no&favc=no&fcvc=2&ncp=3&caec=Sometimes&smoke=no&ch2o=2&scc=no&faf=2&tue=1&calc=no&mtrans=Walking"
```

### Using Python requests

```python
import requests

data = {
    'gender': 'Male',
    'age': 25,
    'height': 1.75,
    'weight': 70,
    'family_history_with_overweight': 'no',
    'favc': 'no',
    'fcvc': 2,
    'ncp': 3,
    'caec': 'Sometimes',
    'smoke': 'no',
    'ch2o': 2,
    'scc': 'no',
    'faf': 2,
    'tue': 1,
    'calc': 'no',
    'mtrans': 'Walking'
}

response = requests.post('http://localhost:5000/predict', data=data)
print(response.text)
```

## Error Handling

The API handles the following error scenarios:

- **Missing required fields**: Returns 400 Bad Request
- **Invalid data types**: Returns 400 Bad Request
- **Model loading errors**: Returns 500 Internal Server Error
- **Prediction errors**: Returns 500 Internal Server Error

## Rate Limiting

Currently, no rate limiting is implemented. Consider implementing rate limiting for production use.

## Security Considerations

- Input validation is performed on all form fields
- SQL injection protection (no database queries)
- XSS protection through Flask's built-in security features
- Consider implementing HTTPS for production deployments

## Future Enhancements

- JSON API endpoints
- Authentication and authorization
- Rate limiting
- Request/response logging
- API versioning
- Swagger/OpenAPI documentation 