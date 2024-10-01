export default function ButtonNewChat(props) {
    console.log(props.selectItem)

    return (
        <div class="flex place-content-end p-2">
            <button
                onClick={() => props.selectItem('form')}
            ><svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="2.5"
                stroke="white"
                height="15"
                width="20"

            >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M12 4.5v15m7.5-7.5h-15"></path>
                </svg></button>
        </div>
    )
}


