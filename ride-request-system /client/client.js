// client/client.js
const axios = require('axios');

const SERVER_URL = 'http://localhost:3000';

// Client API function to submit ride request
async function submitRideRequest(sourceLocation, destLocation, userId) {
  try {
    console.log('\n🚗 Submitting ride request...');
    console.log('Source:', sourceLocation);
    console.log('Destination:', destLocation);
    console.log('User ID:', userId);

    const response = await axios.post(`${SERVER_URL}/api/ride-request`, {
      source_location: sourceLocation,
      dest_location: destLocation,
      user_id: userId
    });

    console.log('\n✅ Success!');
    console.log('Response:', response.data);
    return response.data;

  } catch (error) {
    console.error('\n❌ Error submitting ride request:');
    if (error.response) {
      console.error('Status:', error.response.status);
      console.error('Message:', error.response.data);
    } else {
      console.error('Message:', error.message);
    }
    throw error;
  }
}

// Client API function to get all ride requests
async function getAllRideRequests() {
  try {
    console.log('\n📋 Fetching all ride requests...');
    
    const response = await axios.get(`${SERVER_URL}/api/ride-requests`);
    
    console.log('\n✅ Success!');
    console.log(`Found ${response.data.count} ride requests`);
    console.log('Data:', JSON.stringify(response.data.data, null, 2));
    return response.data;

  } catch (error) {
    console.error('\n❌ Error fetching ride requests:');
    console.error('Message:', error.message);
    throw error;
  }
}

// Example usage - you can modify these values
async function main() {
  // Check command line arguments
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('\n📖 Usage:');
    console.log('Submit ride: node client.js submit <source> <destination> <user_id>');
    console.log('Get all rides: node client.js getall');
    console.log('\nExample: node client.js submit "123 Main St" "456 Oak Ave" "user123"');
    return;
  }

  const command = args[0];

  if (command === 'submit') {
    if (args.length < 4) {
      console.error('❌ Error: Missing parameters');
      console.log('Usage: node client.js submit <source> <destination> <user_id>');
      return;
    }
    
    const [, source, dest, userId] = args;
    await submitRideRequest(source, dest, userId);
    
  } else if (command === 'getall') {
    await getAllRideRequests();
    
  } else {
    console.error('❌ Unknown command:', command);
    console.log('Available commands: submit, getall');
  }
}

// Run the main function
main().catch(err => {
  console.error('Fatal error:', err.message);
  process.exit(1);
});

// Export functions for use in other files or testing
module.exports = {
  submitRideRequest,
  getAllRideRequests
};

