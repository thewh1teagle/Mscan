import styled from '@emotion/styled';
import { Box, Typography } from '@mui/material';
import React from 'react';
import './App.css';
import ResultCards from './components/ResultCards';
import { Status } from './components/ResultCards';
import { SelectInterface } from './components/SelectInterface';
import LoadingButton from '@mui/lab/LoadingButton';

// Point Eel web socket to the instance
export const eel = window.eel
eel.set_host( 'ws://localhost:8888' )



const Header = styled('div')`
  margin-top: 20px;
`

const App = () => {
  const [currentInterface, setCurrentInterface] = React.useState({});
  const [scanState, setScanState] = React.useState<Status[]>([
    // ...Array(15).fill({
    //   ip: '10.0.0.1',
    //   mac: 'aa:bb:cc:dd:ee:ff',
    //   hostname: 'hostname',
    //   vendor: 'Xiaomi',
    // })
  ]);
  const [loading, setLoading] = React.useState(false);


  const scan = () => {
    setScanState([]);
    setLoading(true)
    const intervalId = setInterval(() => {
      const progress = eel.progress()
      console.log('hi from interval')
      console.log(progress)
    }, 1000)
    eel.scan(currentInterface)((result: Status[]) => {
      setScanState(result)
      setLoading(false)
    })
    clearInterval(intervalId)
  }
  return (
    <>
    <Header>
      <Typography variant="h4" textAlign="center" fontWeight="bold" color="#1f1a56" padding="0 0 20px 0px">
      Nwpy Scanner
      </Typography>
    </Header>
    <Box sx={{
      display: 'flex',
      flexDirection: 'column',
      margin: 'auto',
      width: '20%',
    }}>
      <SelectInterface currentInterface={currentInterface} setCurrentInterface={setCurrentInterface} />
      <LoadingButton loading={loading} variant="contained" onClick={scan}>Scan</LoadingButton>
      
    </Box>
    
    {
      <ResultCards result={scanState} loading={loading} />
    }
    </>
  )
}


export default App;
