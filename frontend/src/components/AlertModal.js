import React, { useState } from 'react';
import {
  Dialog, DialogTitle, DialogContent, DialogActions,
  Button, TextField, Select, MenuItem, FormControl,
  InputLabel, RadioGroup, FormControlLabel, Radio
} from '@mui/material';

export const AlertModal = ({ open, onClose, onSubmit, cryptocurrencies }) => {
  const [formData, setFormData] = useState({
    crypto: 'BTC',
    email: '',
    targetPrice: '',
    above: true
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <form onSubmit={handleSubmit}>
        <DialogTitle>Set Price Alert</DialogTitle>
        <DialogContent>
          <FormControl fullWidth margin="normal">
            <InputLabel>Cryptocurrency</InputLabel>
            <Select
              value={formData.crypto}
              onChange={(e) => setFormData({ ...formData, crypto: e.target.value })}
            >
              {cryptocurrencies.map(crypto => (
                <MenuItem key={crypto} value={crypto}>{crypto}</MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField
            fullWidth
            margin="normal"
            label="Email"
            type="email"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          />
          <TextField
            fullWidth
            margin="normal"
            label="Target Price (USD)"
            type="number"
            step="0.01"
            value={formData.targetPrice}
            onChange={(e) => setFormData({ ...formData, targetPrice: e.target.value })}
          />
          <RadioGroup
            value={formData.above}
            onChange={(e) => setFormData({ ...formData, above: e.target.value === 'true' })}
          >
            <FormControlLabel value={true} control={<Radio />} label="Alert when price goes above" />
            <FormControlLabel value={false} control={<Radio />} label="Alert when price goes below" />
          </RadioGroup>
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Cancel</Button>
          <Button type="submit" variant="contained">Set Alert</Button>
        </DialogActions>
      </form>
    </Dialog>
  );
};
