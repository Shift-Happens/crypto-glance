import React, { useState } from 'react';
import { Paper, TextField, Button, Box } from '@mui/material';

export const AddressSearch = ({ onSearch }) => {
  const [address, setAddress] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(address);
  };

  return (
    <Paper component="form" onSubmit={handleSubmit} sx={{ p: 2, mb: 3 }}>
      <Box sx={{ display: 'flex', gap: 2 }}>
        <TextField
          fullWidth
          label="Bitcoin Address"
          value={address}
          onChange={(e) => setAddress(e.target.value)}
        />
        <Button type="submit" variant="contained">Search</Button>
      </Box>
    </Paper>
  );
};
