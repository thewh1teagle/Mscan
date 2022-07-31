import React from 'react';
import { Status } from './ResultCards';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { Skeleton } from '@mui/material';


interface ResultCardProps {
    status: Status
}

interface InfoCellProps {
    label: string,
    value: string
}
const InfoCell: React.FC<InfoCellProps> = ({label, value}) => {
    return (
        <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" padding={2} color="#aab1c4" minWidth="20%">
            <Typography color="#909ab2" variant="h6" fontWeight="bold">{value}</Typography>
            <Typography fontSize="1em" fontWeight="500">{label}</Typography>            
        </Box>
    )
}


const ResultCard: React.FC<ResultCardProps> = ({ status }) => {
    return (

        <Box sx={{
            display: 'flex',
            flexDirection: 'row',
            alignItems: 'center',
            justifyContent: 'space-around',
            borderRadius: '10px',
            boxShadow: '0px 0px 10px 0px rgba(0,0,0,0.2)',
            width: '100%',
            height: '100px'
        }}>
            {
                status.ip !== '' ? (
                    <>
                    <InfoCell label="IP" value={status.ip} />
                    <InfoCell label="MAC" value={status.mac} />
                    {/* <InfoCell label="MAC" value="aa:bb:cc:dd:ee:ff" /> */}
                    <InfoCell label="Vendor" value={status.vendor} />
                    <InfoCell label="Hostname" value={status.hostname} />
                    </>
                )
                    : (
                        <>
                        <Skeleton variant="rectangular" width='100%' height='100%' />
                        </>
                    )
            }
          
        </Box>

    );
}

export default ResultCard;
















