import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

const products = {
  'steuer-tracker': { name: 'Steuer-Tracker 2026', price: 4700 },
  'rechnungs-generator': { name: 'Rechnungs-Generator Pro', price: 3700 },
  'content-kalender': { name: 'Content-Kalender', price: 2700 },
  'preiskalkulator': { name: 'Preiskalkulator', price: 1700 },
  'vertragsvorlagen': { name: 'Vertragsvorlagen', price: 3700 },
  'finanz-dashboard': { name: 'Finanz-Dashboard', price: 6700 },
  'steuer-masterclass': { name: 'Steuer-Masterclass', price: 9700 },
  'notion-pm': { name: 'Notion PM-Template', price: 2900 },
  'email-vorlagen': { name: 'Email-Vorlagen', price: 1900 },
  'linkedin-optimizer': { name: 'LinkedIn Optimizer', price: 3900 },
};

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { productId } = req.body;

  if (!productId || !products[productId]) {
    return res.status(400).json({ error: 'Invalid product ID' });
  }

  const product = products[productId];

  try {
    // Erstelle dynamische Checkout Session
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [
        {
          price_data: {
            currency: 'eur',
            product_data: {
              name: product.name,
            },
            unit_amount: product.price,
          },
          quantity: 1,
        },
      ],
      mode: 'payment',
      success_url: 'https://freelancer-tools.dev/success?session_id={CHECKOUT_SESSION_ID}',
      cancel_url: 'https://freelancer-tools.dev/',
    });

    return res.status(200).json({ url: session.url });
  } catch (error) {
    console.error('Stripe error:', error);
    return res.status(500).json({ error: error.message });
  }
}
