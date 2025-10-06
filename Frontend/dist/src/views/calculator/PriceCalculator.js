import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import Select from "react-select";
import {
  setClassLevel,
  setOriginalPrice,
  setDiscount,
  reset,
  fetchCalculatePrice,
  fetchClassList,
} from "../../redux/calculatorSlice";

// ✅ NEW imports from reactstrap
import { Label, Input, Button } from "reactstrap";

const PriceCalculator = () => {
  const dispatch = useDispatch();
  const {
    classLevel,
    classList,
    originalPrice,
    discount,
    finalPrice,
    error,
    success,
    loading,
  } = useSelector((state) => state.calculator);

  const [previewPrice, setPreviewPrice] = useState("");
  const [warning, setWarning] = useState("");
  const [submitted, setSubmitted] = useState(false); // ✅ Added to track submission

  useEffect(() => {
    dispatch(fetchClassList());
  }, [dispatch]);

  useEffect(() => {
    const priceNum = parseFloat(originalPrice);
    const discountNum = parseFloat(discount);

    if (!isNaN(priceNum) && !isNaN(discountNum)) {
      const calcPrice =
        Math.round(
          (priceNum - priceNum * (discountNum / 100) + Number.EPSILON) * 100
        ) / 100;
      setPreviewPrice(calcPrice.toFixed(2));
    } else {
      setPreviewPrice("");
    }
  }, [originalPrice, discount]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!classLevel || !originalPrice || !discount) {
      setWarning("⚠ Please fill out all the fields.");
      return;
    }
    setWarning("");
    setSubmitted(true); // ✅ Mark form as submitted

    dispatch(
      fetchCalculatePrice({
        class_id: parseInt(classLevel, 10),
        original_price: parseFloat(originalPrice),
        discount_percentage: parseFloat(discount),
        final_price: parseFloat(previewPrice),
      })
    );
  };

  // ✅ New useEffect to clear fields after successful calculation
  useEffect(() => {
    if (!loading && submitted && !error && success) {
      dispatch(reset());           // clears Redux state
      setWarning("");              // clear warning
      setSubmitted(false);         // reset submission state
    }
  }, [loading, submitted, error, success, dispatch]);

  const classOptions = (classList || []).map((cls) => ({
    value: cls.id,
    label: cls.name,
  }));

  return (
    <div className="px-2 price-calculator">
      <h2
        className="mt-0 mb-2 text-center"
        style={{
          fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
          fontWeight: 700,
          fontSize: "2.3rem",
          letterSpacing: "0.5px",
        }}
      >
        Price Calculator
      </h2>

      {(warning || success || error) && (
        <div
          className={`mx-auto mb-1 p-1 text-center fw-bold rounded ${
            warning
              ? "bg-light-warning text-dark"
              : success
              ? "bg-light-success text-white"
              : "bg-light-danger text-white"
          }`}
          style={{ maxWidth: "600px" }}
        >
          {warning ||
            (success ? "✅ Data Calculated successfully!" : `❌ ${error}`)}
        </div>
      )}

      <div
        style={{
          width: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        {/* Class */}
        <div
          className="mb-3 class-field-wrapper"
          style={{ maxWidth: "700px", width: "100%" }}
        >
          <Label for="class-select" className="form-label fs-6 fw-bold">
            Class
          </Label>
          <Select
            inputId="class-select"
            classNamePrefix="select"
            options={classOptions}
            value={
              classOptions.find((option) => option.value === classLevel) || null
            }
            onChange={(option) => dispatch(setClassLevel(option?.value))}
            placeholder="Select Class"
            isSearchable={false}
            noOptionsMessage={() =>
              loading ? "Loading classes..." : "No classes found"
            }
            isDisabled={loading}
          />
        </div>

        {/* Original Price */}
        <div className="mb-3" style={{ maxWidth: "700px", width: "100%" }}>
          <Label for="original-price" className="form-label fs-6 fw-bold mt-0">
            Original Price (₹)
          </Label>
          <Input
            id="original-price"
            type="text"
            className="price-calculator-field"
            value={originalPrice}
            onChange={(e) => {
              const value = e.target.value;
              if (/^\d*\.?\d*$/.test(value)) {
                dispatch(setOriginalPrice(value));
              }
            }}
            placeholder="Enter original price"
          />
        </div>

        {/* Discount */}
        <div className="mb-3" style={{ maxWidth: "700px", width: "100%" }}>
          <Label for="discount" className="form-label fs-6 fw-bold">
            Discount (%)
          </Label>
          <Input
            id="discount"
            type="text"
            className="price-calculator-field"
            value={discount}
            onChange={(e) => {
              const value = e.target.value;
              if (/^\d*\.?\d*$/.test(value)) {
                dispatch(setDiscount(value));
              }
            }}
            placeholder="Enter discount percentage"
          />
        </div>

        {/* Final Price */}
        <div className="mb-3" style={{ maxWidth: "700px", width: "100%" }}>
          <Label for="final-price" className="form-label fs-6 fw-bold">
            Final Price (₹)
          </Label>
          <Input
            id="final-price"
            type="text"
            className="price-calculator-field"
            value={
              finalPrice
                ? `₹${finalPrice}`
                : previewPrice
                ? `₹${previewPrice}`
                : ""
            }
            readOnly
            placeholder="Final price will be shown"
            style={{ backgroundColor: "#f9f9f9" }}
          />
        </div>

        {/* Submit */}
        <Button
          type="button"
          onClick={handleSubmit}
          color="primary"
          disabled={loading}
          className="mb-0"
          style={{ padding: "0.9rem", maxWidth: "200px", width: "100%" }}
        >
          {loading ? "Submit" : "Submit"}
        </Button>
      </div>
    </div>
  );
};

export default PriceCalculator;
