# LinkedIn Buttons Implementation - Dev Branch

## Overview
Successfully implemented LinkedIn buttons in the "quem-somos" page for users who have LinkedIn profiles stored in DynamoDB. The implementation follows the MMIV blue color scheme and includes comprehensive functionality for managing LinkedIn profiles.

## Features Implemented

### ✅ Core Functionality
- **Conditional Display**: LinkedIn buttons only appear for team members who have a `linkedin` field in their DynamoDB profile
- **DynamoDB Integration**: Direct AWS SDK integration for real-time data fetching from DataIESB-Team table
- **Fallback Support**: Automatic fallback to static data with sample LinkedIn profiles if AWS is unavailable
- **Update Functionality**: Built-in method to add/update LinkedIn profiles in DynamoDB

### ✅ Visual Design
- **MMIV Blue Styling**: LinkedIn buttons use blue color scheme (#007bff) following MMIV style guidelines
- **Professional Appearance**: Clean, modern button design with LinkedIn icon and text
- **Hover Effects**: Smooth transitions with darker blue hover state (#0056b3)
- **Responsive Design**: Mobile-optimized styling with appropriate sizing for different screen sizes

### ✅ Technical Implementation
- **AWS SDK Integration**: Added AWS SDK script to quem-somos.html for DynamoDB access
- **Security**: LinkedIn links open in new tab with `rel="noopener noreferrer"` attributes
- **Performance**: Efficient rendering with conditional logic to avoid empty elements
- **Accessibility**: Proper semantic HTML structure and keyboard navigation support

## Files Modified

### 1. `/src/js/team-data.js`
- Already contained comprehensive LinkedIn functionality
- `generateLinkedInLink()` method creates LinkedIn buttons conditionally
- `updateLinkedInProfile()` method for managing LinkedIn profiles in DynamoDB
- Fallback data includes sample LinkedIn profiles for testing

### 2. `/src/style/team-dynamic.css`
- Added LinkedIn button styling with MMIV blue color scheme
- Responsive design rules for mobile devices
- Print-friendly styles for LinkedIn buttons
- Hover effects and smooth transitions

### 3. `/src/quem-somos.html`
- Added AWS SDK script for DynamoDB integration
- Maintains existing team grid structure

### 4. `/src/test-linkedin-dev.html` (New)
- Comprehensive test page demonstrating LinkedIn functionality
- Examples of team members with and without LinkedIn profiles
- Live DynamoDB integration testing
- Technical documentation and usage examples

## Data Structure

LinkedIn profiles are stored in DynamoDB with this structure:
```json
{
  "id": "1",
  "email": "sergio.cortes@iesb.edu.br",
  "name": "Professor Sérgio da Costa Côrtes",
  "role": "Coordenação",
  "category": "Coordenação",
  "linkedin": "https://www.linkedin.com/in/sergio-cortes-iesb",
  "active": true
}
```

## Usage Examples

### Adding LinkedIn Profile via JavaScript
```javascript
const teamManager = new TeamDataManager();
await teamManager.updateLinkedInProfile('3', 'https://www.linkedin.com/in/natalia-evangelista');
```

### Adding LinkedIn Profile via AWS CLI
```bash
aws dynamodb update-item \
  --table-name DataIESB-Team \
  --key '{"id":{"S":"3"}}' \
  --update-expression "SET linkedin = :linkedin, updatedAt = :updatedAt" \
  --expression-attribute-values '{
    ":linkedin":{"S":"https://www.linkedin.com/in/natalia-evangelista"},
    ":updatedAt":{"S":"2025-08-10T15:39:00.000Z"}
  }'
```

## Testing

### Test Page Available
- Access `/test-linkedin-dev.html` to see LinkedIn functionality in action
- Demonstrates both team members with and without LinkedIn profiles
- Shows live DynamoDB integration with fallback support

### Sample Data
The fallback data includes LinkedIn profiles for:
- Professor Sérgio da Costa Côrtes
- Professora Simone de Araújo Góes Assis
- Roberto Moreira Diniz
- Marley Abe Silva
- Leonardo Araújo Pereira
- Guilherme Rocha Duarte
- Pedro Martins Rodrigues
- William Wallace Ribeiro Matos

## Deployment Notes

1. **AWS Configuration**: Ensure AWS credentials are properly configured for DynamoDB access
2. **Table Structure**: Verify DataIESB-Team table exists with proper schema
3. **CORS Settings**: Configure CORS if accessing from different domains
4. **Fallback Testing**: Test fallback functionality when AWS is unavailable

## Future Enhancements

- Admin interface for managing LinkedIn profiles
- Bulk import/export functionality
- LinkedIn profile validation
- Analytics tracking for LinkedIn clicks
- Integration with other social media platforms

## Commit Information
- **Branch**: dev
- **Commit**: 9a69eaf
- **Date**: 2025-08-10
- **Files Changed**: 2 files, 229 insertions
