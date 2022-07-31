import styled from '@emotion/styled'
import { Typography } from '@mui/material'
import React from 'react'
import ResultCard from './ResultCard'
import { ReactComponent as EmptyIcon } from '../svgs/empty.svg';


export interface Status {
    ip: string,
    mac: string,
    vendor: string,
    hostname: string,
}


interface ScanResultProps {
    result: Status[],
    loading: boolean,
}

const ResultContainer = styled('div')`
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

`

const ResultCards: React.FC<ScanResultProps> = ({ result, loading }) => {
    console.log(`result length: ${result.length} loading: ${loading}`)

    
    return (
        <ResultContainer>
            {
             result.length === 0 && loading && Array(5).fill({ip: '', mac: '', vendor: '', hostname: ''}).map((status: Status) => (
                <ResultCard key={status.mac} status={status} />
             ))
            }
            {result.length === 0 && !loading && (
                <>
                    <EmptyIcon style={{ width: '30%', height: '30%' }} />
                    <Typography variant="h5" fontWeight="light" color="#1f1a56" padding="0 0 20px 40px">
                        No Scan Results
                    </Typography>
                </>
            )}
            {result.length > 0 && result.map((status: Status) => (
                <ResultCard key={status.mac} status={status} />
            ))}
        </ResultContainer>
    )
}

export default ResultCards