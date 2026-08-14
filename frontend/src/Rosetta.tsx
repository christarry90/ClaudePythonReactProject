import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm';
import { useEffect } from 'react';
import {useState} from 'react';

function ReadRosetta() {
    const [content, setContent] = useState<string>();
    useEffect(() => {
    async function fetchRosetta() {
      try {
        const response = await fetch('/proxy/8000/readRosetta');

        if (!response.ok) {
          throw new Error('Failed to read file');
        }

        const data: string = (await response.json()).content;
        setContent(data);
      } catch (error) {
        console.error(error);
      }
    }

    fetchRosetta();
  }, []);

  return (
    <>
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
    </>
    
  );
}

export default ReadRosetta;