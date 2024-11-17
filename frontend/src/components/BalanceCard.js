import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';

export const BalanceCard = ({ balance, usdBalance }) => {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>Balance</Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <Typography variant="h4">{balance.toFixed(8)} BTC</Typography>
          <Typography variant="subtitle1" color="text.secondary">
            ${usdBalance.toFixed(2)} USD
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};
