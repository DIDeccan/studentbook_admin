import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
// import axios from 'axios'; // 

const PriceCalculator = () => {
  const [classLevel, setClassLevel] = useState('');
  const [originalPrice, setOriginalPrice] = useState('');
  const [discount, setDiscount] = useState('');
  const [finalPrice, setFinalPrice] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Calculate final price whenever originalPrice or discount changes
  useEffect(() => {
    if (originalPrice && discount) {
      const price = parseFloat(originalPrice);
      const discountPercent = parseFloat(discount);
      if (!isNaN(price) && !isNaN(discountPercent)) {
        const discountAmount = price * (discountPercent / 100);
        const calculatedPrice = price - discountAmount;
        setFinalPrice(calculatedPrice.toFixed(2));
      } else {
        setFinalPrice(null);
      }
    } else {
      setFinalPrice(null);
    }
  }, [originalPrice, discount]);

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // Validate form inputs
    if (!classLevel || !originalPrice || !discount || !finalPrice) {
      setError('Please fill in all fields correctly.');
      return;
    }

    // ✅ For now, just show alert with data instead of sending to backend
    alert(
      `Class: ${classLevel}\nOriginal Price: ₹${originalPrice}\nDiscount: ${discount}%\nFinal Price: ₹${finalPrice}`
    );

    setSuccess('Data ready to be submitted!');

    // Reset form after alert
    setClassLevel('');
    setOriginalPrice('');
    setDiscount('');
    setFinalPrice(null);

    /*
    // ❌ Commented: Actual backend call
    try {
      const payload = {
        class: classLevel,
        originalPrice: parseFloat(originalPrice),
        discount: parseFloat(discount),
        finalPrice: parseFloat(finalPrice),
      };

      const response = await axios.post('https://your-backend.com/api/submit', payload, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      setSuccess('Data submitted successfully!');
      console.log('Backend Response:', response.data);
    } catch (err) {
      setError('Failed to submit data. Please try again.');
      console.error('API Error:', err.response?.data || err.message);
    }
    */
  };

  return (
    <div className="d-flex align-items-center justify-content-center py-4">
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-12 col-md-5">
            <div className="card shadow-sm" style={{ minHeight: '550px' }}>
              <div className="card-body d-flex flex-column align-items-center p-5">
                <h1 className="card-title h5 fw-bold mb-5 text-center">Price Calculator</h1>
                {error && <div className="alert alert-danger text-center w-100 mb-4">{error}</div>}
                {success && <div className="alert alert-success text-center w-100 mb-4">{success}</div>}
                <div className="w-100" style={{ maxWidth: '450px' }}>
                  <div className="mb-4">
                    <label className="form-label text-left fs-6 d-block fw-bold">Class</label>
                    <select
                      className="form-select"
                      value={classLevel}
                      onChange={(e) => setClassLevel(e.target.value)}
                    >
                      <option value="">Select Class</option>
                      {[6, 7, 8, 9, 10].map((cls) => (
                        <option key={cls} value={cls}>Class {cls}</option>
                      ))}
                    </select>
                  </div>
                  <div className="mb-4">
                    <label className="form-label text-left fs-6 d-block fw-bold">Original Price (₹)</label>
                    <input
                      type="number"
                      className="form-control"
                      value={originalPrice}
                      onChange={(e) => setOriginalPrice(e.target.value)}
                      placeholder="Enter original price"
                      min="0"
                      step="0.01"
                    />
                  </div>
                  <div className="mb-4">
                    <label className="form-label text-left fs-6 d-block fw-bold">Discount (%)</label>
                    <input
                      type="number"
                      className="form-control"
                      value={discount}
                      onChange={(e) => setDiscount(e.target.value)}
                      placeholder="Enter discount percentage"
                      min="0"
                      max="100"
                      step="0.01"
                    />
                  </div>
                  <div className="mb-4">
                    <label className="form-label text-left fs-6 d-block fw-bold ">Final Price (₹)</label>
                    <input
                      type="text"
                      className="form-control bg-light"
                      value={finalPrice ? `₹${finalPrice}` : ''}
                      readOnly
                      placeholder="Final price will be calculated"
                    />
                  </div>
                  <button
                    type="button"
                    onClick={handleSubmit}
                    className="btn btn-primary w-100 mt-4"
                  >
                    Submit
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PriceCalculator;
