import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Stack,
} from "@mui/material";
import React, { useEffect } from "react";
import * as api from "../Api";
import ErrorModal from "./ErrorModal";

interface SelectInterfaceProps {
  currentInterface: any;
  setCurrentInterface: React.Dispatch<React.SetStateAction<any>>;
}

export const SelectInterface: React.FC<SelectInterfaceProps> = ({
  currentInterface,
  setCurrentInterface,
}) => {
  const [interfaces, setInterfaces] = React.useState<any[]>([]);
  const [modalData, setModalData] = React.useState({
    show: false,
    title: "",
    desc: "",
  });

  useEffect(() => {
    async function loadInterfaces() {
      const res = await api.getInterfaces();
      setInterfaces(res.interfaces);
      setCurrentInterface(res.default ?? null);
    }
    loadInterfaces();
  }, [setCurrentInterface]);

  const currentInterfaceIdx =
    interfaces.findIndex((i) => i.name === currentInterface.name) || 0;

  function onInterfaceChange(e: any) {
    const selected = interfaces[e.target.value as number];
    const prefix_length = selected.prefix_length as string;
    if (prefix_length !== '24') {
        setModalData({show: true, title: "Warning", desc: `Large network detected, scanning may take time. Consider selecting a smaller network or narrowing IP range, or choose another interface.`})
    }
    setCurrentInterface(selected);
  }

  return (
    <Stack>
      {modalData.show && (
        <ErrorModal
          title={modalData.title}
          desc={modalData.desc}
          onClose={() => setModalData({ ...modalData, show: false })}
        />
      )}
      <FormControl fullWidth>
        <InputLabel>Interface</InputLabel>
        <Select
          label="Interface"
          onChange={onInterfaceChange}
          value={currentInterfaceIdx}
        >
          {interfaces.map((i, idx) => (
            <MenuItem key={i.name} value={idx}>
              {i.name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </Stack>
  );
};
