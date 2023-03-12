import { Textarea, Button } from '@chakra-ui/react';

function Prompter() {
  return (
    <>
      <Textarea my={5} placeholder="Enter a question" width="full" height="200px" resize={'none'} />
      <Textarea placeholder="Enter keywords" width="full" height="100px" resize={'none'} />
      <Button colorScheme={'red'} width="full" my={5}>
        Check
      </Button>
    </>
  );
}

export default Prompter;
