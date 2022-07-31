import { FormControl, InputLabel, MenuItem, Select } from "@mui/material"
import React, { useEffect } from "react";
import { eel } from "../App";




interface SelectInterfaceProps {
    currentInterface: string,
    setCurrentInterface: React.Dispatch<React.SetStateAction<string>>,
}

export const SelectInterface: React.FC<SelectInterfaceProps> = ({currentInterface, setCurrentInterface}) => {
    const [interfaces, setInterfaces] = React.useState<string[]>([]);
    useEffect(() => {
        eel.listInterfaces()((result: string[]) => {
            setInterfaces(result);
        })
        eel.defaultInterface()((default_interface: string) => {
            setCurrentInterface(default_interface);
        })
    }, [setCurrentInterface])
    return (
        <>
            <FormControl fullWidth>
                <InputLabel id="demo-simple-select-label">Interface</InputLabel>
                <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={currentInterface}
                    label="Interface"
                    onChange={e => setCurrentInterface(e.target.value)}
                >
                    {interfaces.map((i: any) => (
                        <MenuItem key={i.name} value={i.name}>{i.name}</MenuItem>
                    ))}
                </Select>
            </FormControl>
        </>
    )
}