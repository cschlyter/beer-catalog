import React from "react";

import { sanitize } from "dompurify";
import { Card } from "react-bootstrap";

function ResultListItem({ result }) {
  return (
    <Card className="mb-3">
      <Card.Body>
        <Card.Title>
          {result.name} | {result.style} | {result.brewery}
        </Card.Title>
        <Card.Subtitle className="mb-2 text-muted">
          Country: {result.country} | {result.points} Points | ${result.price}
        </Card.Subtitle>
        <Card.Text>{sanitize(result.description)}</Card.Text>
      </Card.Body>
    </Card>
  );
}

export default ResultListItem;
