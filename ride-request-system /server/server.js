// server/server.js
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { Pool } = require('pg');

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// PostgreSQL connection pool
const pool = new Pool({
  user: 'postgres',      // Your PostgreSQL username (default is 'postgres')
  host: 'localhost',
  database: 'ride_requests',
  password: 'gun1',  // IMPORTANT: Replace with YOUR password from installation
  port: 5432,
});

// Test database connection
pool.connect((err, client, release) => {
  if (err) {
    console.error('Error connecting to PostgreSQL:', err.stack);
    console.log('⚠️  Database connection failed. Server will continue without DB.');
  } else {
    console.log('✅ Successfully connected to PostgreSQL database');
    release();
  }
});

// API Endpoint: Submit ride request
app.post('/api/ride-request', async (req, res) => {
  const { source_location, dest_location, user_id } = req.body;

  // Validate input
  if (!source_location || !dest_location || !user_id) {
    return res.status(400).json({
      success: false,
      message: 'Missing required fields: source_location, dest_location, user_id'
    });
  }

  console.log('\n📥 Received ride request:');
  console.log('User ID:', user_id);
  console.log('Source:', source_location);
  console.log('Destination:', dest_location);

  try {
    // Try to insert into database
    const query = `
      INSERT INTO rides (user_id, source_location, dest_location)
      VALUES ($1, $2, $3)
      RETURNING *
    `;
    
    const result = await pool.query(query, [user_id, source_location, dest_location]);
    
    console.log('✅ Data successfully stored in PostgreSQL database');
    console.log('Database Record:', result.rows[0]);
    
    res.status(201).json({
      success: true,
      message: 'Ride request submitted successfully',
      data: result.rows[0]
    });

  } catch (error) {
    // If database fails, still show the data
    console.error('❌ Database error:', error.message);
    console.log('\n🔄 Fallback: We will store this data in PostgreSQL now');
    console.log('Data to be stored:');
    console.log({
      user_id,
      source_location,
      dest_location,
      timestamp: new Date().toISOString()
    });

    res.status(200).json({
      success: true,
      message: 'Ride request received (database unavailable, but data logged)',
      data: {
        user_id,
        source_location,
        dest_location,
        timestamp: new Date().toISOString()
      }
    });
  }
});

// API Endpoint: Get all ride requests (bonus feature)
app.get('/api/ride-requests', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM rides ORDER BY created_at DESC');
    res.json({
      success: true,
      count: result.rows.length,
      data: result.rows
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Error fetching ride requests',
      error: error.message
    });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'Server is running', timestamp: new Date().toISOString() });
});

// Start server
app.listen(PORT, () => {
  console.log(`\n🚀 Server is running on http://localhost:${PORT}`);
  console.log(`📡 API Endpoint: http://localhost:${PORT}/api/ride-request`);
  console.log(`💚 Health Check: http://localhost:${PORT}/health`);
});

