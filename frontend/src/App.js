import { useEffect } from "react";
import {
  Routes,
  Route,
  useNavigationType,
  useLocation,
} from "react-router-dom";
import Frame from "./pages/Frame";
import Desktop from "./pages/Desktop";
import Sidebar from "./pages/Sidebar";
import TESTIMONIAL from "./pages/TESTIMONIAL";
import Frame1 from "./pages/Frame1";

function App() {
  const action = useNavigationType();
  const location = useLocation();
  const pathname = location.pathname;

  useEffect(() => {
    if (action !== "POP") {
      window.scrollTo(0, 0);
    }
  }, [action, pathname]);

  useEffect(() => {
    let title = "";
    let metaDescription = "";

    switch (pathname) {
      case "/":
        title = "";
        metaDescription = "";
        break;
      case "/desktop":
        title = "";
        metaDescription = "";
        break;
      case "/sidebar":
        title = "";
        metaDescription = "";
        break;
      case "/testimonial":
        title = "";
        metaDescription = "";
        break;
      case "/5":
        title = "";
        metaDescription = "";
        break;
    }

    if (title) {
      document.title = title;
    }

    if (metaDescription) {
      const metaDescriptionTag = document.querySelector(
        'head > meta[name="description"]'
      );
      if (metaDescriptionTag) {
        metaDescriptionTag.content = metaDescription;
      }
    }
  }, [pathname]);

  return (
    <Routes>
      <Route path="/" element={<Frame />} />
      <Route path="/desktop" element={<Desktop />} />
      <Route path="/sidebar" element={<Sidebar />} />
      <Route path="/testimonial" element={<TESTIMONIAL />} />
      <Route path="/5" element={<Frame1 />} />
    </Routes>
  );
}
export default App;
