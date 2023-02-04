import { Stack, styled, Typography } from "@mui/material";
import { ReactNode, useState } from "react";

const Modal = styled(Stack)({
  position: "absolute",
  justifyContent: "center",
  alignItems: "center",
  left: 0,
  top: 0,
  width: "100vw",
  height: "100vh",
  zIndex: 2,
  background: "rgba(0,0,0,0.5)",
  backdropFilter: "blur(5px)",
});

const Container = styled(Stack)({
  width: "35%",
  height: "40%",
  background: "white",
  boxShadow: "0px 0px 30px 0px",
  borderRadius: "40px",
  padding: "25px",
});

const CustomButtonStyle = styled("button")((props) => ({
  all: "unset",
  width: "83px",
  height: "35px",
  background: "red",
  color: "white",
  borderRadius: "10px",
  textAlign: "center",
  cursor: "pointer",
  fontWeight: "bold",
  padding: "2px 5px",
  position: "relative",
  transition: "transform 0.2s ease",
  ":hover": {
    transform: "scale(1.1)",
    boxShadow: "0px 0px 10px #aaa",
  },
  ...props,
}));

function CopyBtn({ children }: { children: ReactNode }) {
  const [showCopied, setShowCopied] = useState(false);

  function onCopy() {
    setShowCopied(true)
    setTimeout(() => setShowCopied(false), 1000);
  }
  return (
    <CustomButtonStyle
      sx={{ color: "#E9736B", background: "#FCE5E1" }}
      onClick={onCopy}
    >
      {showCopied ? "Copied!" : children}
    </CustomButtonStyle>
  );
}

export default function ErrorModal({
  title,
  desc,
  fullError,
  onClose,
}: {
  title: string;
  desc: string;
  fullError?: string;
  onClose: VoidFunction;
}) {
  const [show, setShow] = useState(true);

  if (!show) {
    return null;
  }

  return (
    <Modal>
      <Container>
        <Typography
          variant="h4"
          fontWeight="bold"
          textAlign="center"
          color="red"
        >
          {title}
        </Typography>
        <Typography
          variant="h6"
          sx={{ fontSize: "0.98em", marginTop: "20px" }}
          fontWeight="bold"
          textAlign="center"
        >
          {desc}
        </Typography>
        <Stack
          direction="row"
          marginTop="auto"
          justifyContent="center"
          gap="10px"
        >
          <CopyBtn>Copy Error</CopyBtn>

          <CustomButtonStyle
            onClick={() => {
              setShow(false);
              onClose();
            }}
            sx={{
              background: "#D8D8D9",
              color: "black",
            }}
          >
            Cancel
          </CustomButtonStyle>
        </Stack>
      </Container>
    </Modal>
  );
}
