import styled from '@emotion/styled';
import { Typography, Stack } from '@mui/material';
import React from 'react';
import Report from './components/Report';
import { Host } from './components/Report';
import { SelectInterface } from './components/SelectInterface';
import LoadingButton from '@mui/lab/LoadingButton';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import * as api from "./Api";


const Header = styled(Typography)({
  marginTop: "20px",
  textAlign: "center",
  fontWeight: "bold",
  color:"#1f1a56",
  padding: "0 0 20px 0px",
  fontSize: "1.8em"
})

const SelectIContainer = styled(Stack)({
  display: 'flex',
  flexDirection: 'column',
  margin: 'auto',
  width: '20%',
})

const App = () => {
  const [currentInterface, setCurrentInterface] = React.useState({});
  const [scanState, setScanState] = React.useState<Host[]>([
    // ...Array(15).fill({
    //   ip: '10.0.0.1',
    //   mac: 'aa:bb:cc:dd:ee:ff',
    //   hostname: 'hostname',
    //   vendor: 'Xiaomi',
    // })
  ]);
  const [loading, setLoading] = React.useState(false);


  const scan = async () => {
    setScanState([]);
    setLoading(true)
    const res = await api.scan(currentInterface)
    setScanState(res)
    setLoading(false)
  }

  return (
    <Stack>
      <Header>
          Mscan
      </Header>
      <SelectIContainer>
        <SelectInterface currentInterface={currentInterface} setCurrentInterface={setCurrentInterface} />
        <LoadingButton loading={loading} variant="contained" onClick={scan}>Scan</LoadingButton>
      </SelectIContainer>
      <Report data={scanState} loading={loading} />
    </Stack>
  )
}


export default App;
