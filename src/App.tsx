import { Container, Heading, Tabs, TabList, Tab, TabPanels, TabPanel } from '@chakra-ui/react';
import Prompter from '@components/Prompter';

function App() {
  return (
    <Container my={5} centerContent>
      <Heading my={10}>Smile NLP Test</Heading>
      <Tabs width="full" variant="soft-rounded" colorScheme="red">
        <TabList mx={5}>
          <Tab>English</Tab>
          <Tab>Korean</Tab>
        </TabList>
        <TabPanels>
          <TabPanel>
            <Prompter option="eng" />
          </TabPanel>
          <TabPanel>
            <Prompter option="kor" />
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Container>
  );
}

export default App;
