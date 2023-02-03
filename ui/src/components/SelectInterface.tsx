import { FormControl, InputLabel, MenuItem, Select, Stack } from "@mui/material"
import React, { useEffect } from "react";
import * as api from '../Api';


interface SelectInterfaceProps {
    currentInterface: any,
    setCurrentInterface: React.Dispatch<React.SetStateAction<any>>,
}

export const SelectInterface: React.FC<SelectInterfaceProps> = ({currentInterface, setCurrentInterface}) => {
    const [interfaces, setInterfaces] = React.useState<any[]>([]);

    useEffect(() => {
        async function loadInterfaces() {
            const res = await api.getInterfaces()
            setInterfaces(res.interfaces)
            setCurrentInterface(res.default)
        }
        loadInterfaces()
    }, [setCurrentInterface])


     const currentInterfaceIdx = interfaces.findIndex(i => i.name === currentInterface.name) || 0

    return (
        <Stack>
            <FormControl fullWidth>
                <InputLabel>Interface</InputLabel>
                <Select
                    label="Interface"
                    onChange={e => setCurrentInterface(interfaces[e.target.value as number])}
                    value={currentInterfaceIdx}
                >
                    {interfaces.map((i, idx) => 
                        <MenuItem key={i.name} value={idx}>{i.name}</MenuItem> 
                    )}
                </Select>
            </FormControl>
        </Stack>
    )
}