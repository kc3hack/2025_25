const ResultField = (props) => {
    const result = props.result

    return (
        <div>
            {result && (
                <div>
                    <h2>判定結果</h2>
                    <pre>{JSON.stringify(result, null, 2)}</pre>
                </div>
            )}
        </div>
    )
}

export default ResultField;