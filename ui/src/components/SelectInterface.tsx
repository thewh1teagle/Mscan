import { FormControl, InputLabel, MenuItem, Select } from "@mui/material"
import React, { useEffect } from "react";
import { eel } from "../App";


interface SelectInterfaceProps {
    currentInterface: any,
    setCurrentInterface: React.Dispatch<React.SetStateAction<any>>,
}

export const SelectInterface: React.FC<SelectInterfaceProps> = ({currentInterface, setCurrentInterface}) => {
    const [interfaces, setInterfaces] = React.useState<any[]>([]);
    useEffect(() => {
        eel.defaultInterface()((default_interface: any) => {
            setCurrentInterface(default_interface);
        })
        eel.listInterfaces()((result: any[]) => {
            setInterfaces(result);
        })

    }, [setCurrentInterface])
    return (
        <>
            <FormControl fullWidth>
                <InputLabel id="demo-simple-select-label">Interface</InputLabel>
                <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    label="Interface"
                    onChange={e => setCurrentInterface(e.target.value)}
                >
                    {interfaces.map((i: any, idx) => {
                        const selected = i.name === currentInterface.name
                        return <MenuItem key={i.name} value={i}>{i.name}</MenuItem>
                    })}
                </Select>
            </FormControl>
        </>
    )
}