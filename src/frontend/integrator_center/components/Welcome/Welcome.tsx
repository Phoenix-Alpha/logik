import { Page, WelcomeCard } from "@components";
import { Col, Row, Space, Typography } from "antd";
import { FC } from "react";
import styled from "styled-components";

const StyledWelcomeWrapper = styled.div`
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  align-items: center;
  justify-content: center;
`;

export interface IWelcomeProps {}

export const Welcome: FC<IWelcomeProps> = ({}: IWelcomeProps) => {
  return (
    <Page>
      <StyledWelcomeWrapper>
        <Space direction="vertical" size="large">
          <Row align="middle" justify="center">
            <Typography.Title level={3}>
              Welcome to the Integrator Center of LogiK by Klocel!
            </Typography.Title>
          </Row>
          <Row gutter={{ xs: 8, sm: 16, md: 24, lg: 32 }} justify="center">
            <Col>
              <WelcomeCard />
            </Col>
            <Col>
              <WelcomeCard />
            </Col>
            <Col>
              <WelcomeCard />
            </Col>
          </Row>
        </Space>
      </StyledWelcomeWrapper>
    </Page>
  );
};

Welcome.displayName = "Welcome";

export default Welcome;
