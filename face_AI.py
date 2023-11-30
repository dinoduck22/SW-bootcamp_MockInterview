import streamlit as st
import streamlit.components.v1 as components


def faceanima():

    with open('./face.css') as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)  # CSS

    html_string = '''
        <div class="face">
          <div class="face__eyes">
            <div class="eye eye--left"></div>
            <div class="eye eye--right"></div>
          </div>
          <div class="face__mouth"></div>
        </div>
    
    
    <script>
        window.addEventListener("pointermove", update);
        const mapRange = (inputLower, inputUpper, outputLower, outputUpper) => {
            const INPUT_RANGE = inputUpper - inputLower;
            const OUTPUT_RANGE = outputUpper - outputLower;
            return (value) => outputLower + (((value - inputLower) / INPUT_RANGE) * OUTPUT_RANGE || 0);
        };
        const FACE = window.querySelector(".face");   
        const BOUNDS = 20;
        const update = ({ x, y }) => {
            const POS_X = mapRange(0, window.innerWidth, -BOUNDS, BOUNDS)(x);
            const POS_Y = mapRange(0, window.innerHeight, -BOUNDS, BOUNDS)(y);
            FACE.style.setProperty("--x", POS_X);
            FACE.style.setProperty("--y", POS_Y);
        };
    </script>  
    '''
    #components.html(html_string) # JavaScript works
    st.markdown(html_string, unsafe_allow_html=True)  # HTML (JavaScript doesn't work)
