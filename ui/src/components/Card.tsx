import React from "react";
import styled from "@emotion/styled";
import { Host } from "./Report";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { Skeleton } from "@mui/material";
import { SxProps } from "@mui/material";

interface CardProps {
  host: Host;
}

interface InfoCellProps {
  label: string;
  value: string;
  sx?: SxProps;
}
const InfoCell: React.FC<InfoCellProps> = ({ label, value, sx }) => {
  return (
    <Box
      display="flex"
      flexDirection="column"
      gap={1}
      alignItems="center"
      justifyContent="center"
      color="#aab1c4"
      minWidth="20%"
    >
      <Typography sx={{ opacity: 0.8 }} fontSize="1em" fontWeight="500">
        {label}
      </Typography>
      <Typography color="#909ab2" variant="h6" sx={sx} fontWeight="bold">
        {value}
      </Typography>
    </Box>
  );
};

const CardContainer = styled(Box)({
  display: "flex",
  flexDirection: "row",
  alignItems: "center",
  justifyContent: "space-around",
  borderRadius: "10px",
  boxShadow: "0px 0px 10px 0px rgba(0,0,0,0.2)",
  width: "100%",
  height: "100px",
});

const Card: React.FC<CardProps> = ({ host }) => {
  if (!host.ip) {
    return <CardContainer><Skeleton variant="rectangular" sx={{borderRadius: "10px"}} width="100%" height="100%"/></CardContainer>
  }

  return (
    <CardContainer>
      <InfoCell label="IP" value={host.ip} sx={{ fontSize: "0.95em" }} />
      <InfoCell label="MAC" value={host.mac} sx={{ fontSize: "0.95em" }} />
      {/* <InfoCell label="MAC" value="aa:bb:cc:dd:ee:ff" /> */}
      <InfoCell label="VENDOR" value={host.vendor} sx={{ fontSize: "0.8em" }} />
      <InfoCell
        label="HOSTNAME"
        value={host.hostname}
        sx={{ fontSize: "0.8em" }}
      />
    </CardContainer>
  );
};

export default Card;
