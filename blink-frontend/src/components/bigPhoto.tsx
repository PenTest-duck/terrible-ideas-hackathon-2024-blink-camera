import { useEffect, useState } from "react";
import ModalImage from "react-modal-image"

const styles = {
    container: {
      display: 'flex',        
      justifyContent: 'center',
      alignItems: 'center',  
      height: '100vh',         
      margin: 0,              
    }
  };

function BigPhoto(){
    const images = require.context('../../public/photo/', false, /\.(png|jpg)$/);
    const firstImage = images.keys().map(image => images(image));
    const numPic = firstImage.length;
    const [currentIndex, setCurrentIndex] = useState(0);

    useEffect(()=>{
        const Id = setInterval(()=>{
            setCurrentIndex(currentIndex== numPic ? 0 : currentIndex+ 1);
        }, 2000);

        return ()=> clearInterval(Id);
    }, [currentIndex]);

    return (
        <div style={styles.container}>
            <ModalImage
                small={firstImage[currentIndex]}
                large={firstImage[currentIndex]}
            />
        </div>
    );
}

export default BigPhoto;