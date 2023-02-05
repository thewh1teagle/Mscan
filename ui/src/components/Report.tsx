import styled from "@emotion/styled";
import { Typography } from "@mui/material";
import React from "react";
import Card from "./Card";
import { ReactComponent as EmptyIcon } from "../svgs/empty.svg";
import { makeid } from "src/utils";

export interface Host {
  ip: string;
  mac: string;
  vendor: string;
  hostname: string;
}

interface ScanResultProps {
  data: Host[];
  loading: boolean;
}

const ReportContainer = styled("div")`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 80%;
  margin-left: auto;
  margin-right: auto;
  margin-top: 40px;
  margin-bottom: 40px;
  gap: 20px;
`;

function MockData() {
  return Array(5)
    .fill({ ip: "", mac: "", vendor: "", hostname: "" }) as [Host]
}

function EmpyIllustrate() {
  return (
    <>
      <EmptyIcon style={{ width: "30%", height: "30%" }} />
      <Typography
        variant="h5"
        fontWeight="light"
        color="#1f1a56"
        padding="0 0 20px 40px"
      >
        No Scan Results
      </Typography>
    </>
  );
}

const Report: React.FC<ScanResultProps> = ({ data, loading }) => {
  if (loading) {
    data = MockData()
  }
  const isEmpty = data.length === 0


  return (
    <ReportContainer>
      {
        isEmpty ?
          <EmpyIllustrate />
        : data.map((host: Host) => <Card key={makeid(5)} host={host} />)
      }
    </ReportContainer>
  );
};
export default Report;
