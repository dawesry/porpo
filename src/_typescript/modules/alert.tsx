import * as React from 'react';
import Box from '@mui/material/Box';
import Alert from '@mui/material/Alert';
import FlagIcon from '@mui/icons-material/Flag';
import Collapse from '@mui/material/Collapse';
import CloseIcon from '@mui/icons-material/Close';
import IconButton from '@mui/material/IconButton';

export default function BasicAlerts() {
  const [open, setOpen] = React.useState(true);

  return (
    <Box sx={{ width: '100%' }}>
      <Collapse in={open}>
        <Alert icon={<FlagIcon fontSize="inherit" />} severity="info"
          action={
              <IconButton
                aria-label="close"
                color="info"
                size="small"
                onClick={() => {
                  setOpen(false);
                }}
              >
                <CloseIcon fontSize="inherit" />
              </IconButton>
            }
          >
          Porpo for Docker is <b>being built.</b> Expect exciting changes soon!
        </Alert>
      </Collapse>
    </Box>
  );
}