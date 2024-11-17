import React from 'react';
import {
  Table, TableBody, TableCell, TableHead, TableRow,
  Paper, TableContainer, Typography
} from '@mui/material';

export const TransactionsTable = ({ transactions }) => {
  return (
    <TableContainer component={Paper}>
      <Typography variant="h6" sx={{ p: 2 }}>Recent Transactions</Typography>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Amount (BTC)</TableCell>
            <TableCell>Amount (USD)</TableCell>
            <TableCell>From</TableCell>
            <TableCell>Time</TableCell>
            <TableCell>Hash</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {transactions.map((tx) => (
            <TableRow key={tx.hash}>
              <TableCell>{tx.amount.toFixed(8)}</TableCell>
              <TableCell>${tx.amount_usd.toFixed(2)}</TableCell>
              <TableCell>{tx.from_addresses.join(', ')}</TableCell>
              <TableCell>{tx.time}</TableCell>
              <TableCell>{tx.hash.substring(0, 8)}...</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
