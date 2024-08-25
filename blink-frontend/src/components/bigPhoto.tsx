import ReactImageGallery from "react-image-gallery";
import "react-image-gallery/styles/css/image-gallery.css";

interface BigPhotoProps {
    images: string[];
}

const BigPhoto = ({ images }: BigPhotoProps) => {
    const mappedImages = images.map((image) => ({ original: image }));

    return (
        <ReactImageGallery items={mappedImages} autoPlay={true} />
    )
}

export default BigPhoto;