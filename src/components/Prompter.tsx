import { Textarea, Button, Text, Box, Alert, AlertIcon } from '@chakra-ui/react';
import { useState } from 'react';
import { Input, SimilarityRes } from 'types/type';
import { fetchData } from 'api/api';

function Prompter() {
  const [input, setInput] = useState<Input>({
    question: '',
    keywords: '',
  });
  const [similairty, setSimilarity] = useState<SimilarityRes>();

  const KeywordInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput((prev) => {
      return { ...prev, keywords: e.target.value };
    });
  };

  // const { data, refetch } = useQuery(['similarity', input], () => fetchData(input), {
  //   refetchOnWindowFocus: false,
  //   enabled: false, // disable this query from automatically running
  // });

  const OnCheckHandle = () => {
    fetchData(input).then((res) => {
      setSimilarity(() => {
        return {
          question: res?.data.question,
          valid: res?.data.valid,
          keywords_result: res?.data.keywords_result,
        };
      });
    });
  };
  console.log(similairty);

  return (
    <>
      <Textarea
        value={input?.question}
        onChange={(e) =>
          setInput((prev) => {
            return { ...prev, question: e.target.value };
          })
        }
        my={5}
        placeholder="Enter a question"
        width="full"
        height="170px"
        resize={'none'}
      />
      <Textarea
        value={input?.keywords}
        onChange={KeywordInputChange}
        placeholder="Enter keywords"
        width="full"
        height="100px"
        resize={'none'}
      />
      <Button onClick={OnCheckHandle} colorScheme={'red'} width="full" my={5}>
        Check
      </Button>
      <Box borderRadius={'md'} bg="red.100" padding={'5'} mb={'5'}>
        <Text>Your question: {similairty?.question}</Text>
      </Box>
      {similairty?.question ? (
        similairty?.valid ? (
          <Alert status="success">
            <AlertIcon />
            Valid
          </Alert>
        ) : (
          <Alert status="error">
            <AlertIcon />
            Unvalid
          </Alert>
        )
      ) : null}
    </>
  );
}

export default Prompter;
