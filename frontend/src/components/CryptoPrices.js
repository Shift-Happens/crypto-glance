import React from 'react';
import { Grid, Paper, Typography, Box } from '@mui/material';

export const CryptoPrices = ({ prices }) => {
  return (
    <Grid container spacing={2}>
      {Object.entries(prices).map(([crypto, price]) => (
        <Grid item xs={12} sm={6} md={2} key={crypto}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 1 }}>
              <img
                src={`/img/crypto/${crypto.toLowerCase()}.png`}
                alt={crypto}
                style={{ width: 24, height: 24, marginRight: 8 }}
              />
              <Typography variant="subtitle1">{crypto}</Typography>
            </Box>
            <Typography variant="h6">${price.toFixed(2)}</Typography>
          </Paper>
        </Grid>
      ))}
    </Grid>
  );
};
