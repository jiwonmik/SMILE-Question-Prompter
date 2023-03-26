import { Container, Heading, Tabs, TabList, Tab, TabPanels, TabPanel } from '@chakra-ui/react';
import Prompter from '@components/Prompter';

function App() {
  return (
    <>
      <Container width="400px" my={5} centerContent>
        <Heading my={10}>Smile NLP Test</Heading>
        <Tabs variant="soft-rounded" colorScheme="red">
          <TabList mx={5}>
            <Tab>English</Tab>
            <Tab>Korean</Tab>
          </TabList>
          <TabPanels>
            <TabPanel>
              <Prompter />
            </TabPanel>
            <TabPanel>
              <Prompter />
            </TabPanel>
          </TabPanels>
        </Tabs>
      </Container>
    </>
  );
}

export default App;
