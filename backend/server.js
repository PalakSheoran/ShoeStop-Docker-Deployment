const express = require('express');
const app = express();
const cors = require('cors');
const dotenv = require('dotenv');
const connectDB = require('./db/connectDB');
const productRoutes = require('./routes/productRoutes');
const userRoutes = require('./routes/userRoutes');
const Products = require('./modal/productSchema');

dotenv.config();

const port = process.env.port || process.env.PORT || 5000;
const mongoURI = process.env.mongoURI || process.env.MONGO_URI || 'mongodb://localhost:27017/shoestop';

app.use(express.json());
app.use(cors());

app.get('/', (req, res) => {
    res.send('ShoeStop API is running...');
});

app.get('/health', (req, res) => {
    res.status(200).json({ status: 'ok', service: 'shoestop-backend', timestamp: new Date() });
});

app.use('/', userRoutes);
app.use('/api', productRoutes);

// Seed initial products if database is empty
const seedProducts = async () => {
    try {
        const count = await Products.countDocuments();
        if (count === 0) {
            console.log('Database empty. Seeding initial ShoeStop products...');
            await Products.insertMany([
                {
                    title: 'Air Max Pulse',
                    company: 'Nike',
                    price: '9999',
                    image: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&auto=format&fit=crop&q=80'
                },
                {
                    title: 'Ultraboost Light',
                    company: 'Adidas',
                    price: '8499',
                    image: 'https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=600&auto=format&fit=crop&q=80'
                },
                {
                    title: 'RS-X Efekt',
                    company: 'Puma',
                    price: '5999',
                    image: 'https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=600&auto=format&fit=crop&q=80'
                },
                {
                    title: 'Classic Leather',
                    company: 'Reebok',
                    price: '4999',
                    image: 'https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=600&auto=format&fit=crop&q=80'
                },
                {
                    title: 'Fresh Foam 1080',
                    company: 'New Balance',
                    price: '11999',
                    image: 'https://images.unsplash.com/photo-1539185441755-769473a23570?w=600&auto=format&fit=crop&q=80'
                },
                {
                    title: 'Chuck 70 Vintage',
                    company: 'Converse',
                    price: '3999',
                    image: 'https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=600&auto=format&fit=crop&q=80'
                }
            ]);
            console.log('Initial products seeded successfully.');
        }
    } catch (seedErr) {
        console.error('Seeding warning:', seedErr.message);
    }
};

const startServer = async () => {
    try {
        await connectDB(mongoURI);
        console.log('connected to db');
        await seedProducts();
        app.listen(port, () => {
            console.log(`server started at ${port}`);
        });
    } catch (error) {
        console.error('Failed to start server:', error);
    }
};

startServer();
